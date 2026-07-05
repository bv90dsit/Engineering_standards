import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { CheckResult, REPO_URL } from './types';

export interface Rule {
    id: string;
    pattern: string;
    excludePattern?: string;
    filePattern: string;
    excludeFilePattern?: string;
    severity: 'error' | 'warning' | 'information';
    message: string;
}

interface RulesFile {
    module: string;
    rules: Rule[];
}

let loadedRules: Rule[] = [];

export function loadRules(extensionPath: string): void {
    loadedRules = [];

    const modulesDir = findModulesDir(extensionPath);
    if (modulesDir) {
        loadRulesFromDir(modulesDir);
    }

    const config = vscode.workspace.getConfiguration('ukGovStandards');
    const additionalModules = config.get<string[]>('additionalModules', []);
    for (const modulePath of additionalModules) {
        const rulesFile = path.join(modulePath, 'rules.json');
        if (fs.existsSync(rulesFile)) {
            loadRulesFile(rulesFile);
        }
    }
}

function findModulesDir(extensionPath: string): string | null {
    // Check workspace first (extension installed alongside the standards repo)
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders) {
        for (const folder of workspaceFolders) {
            const candidate = path.join(folder.uri.fsPath, 'modules');
            if (fs.existsSync(candidate)) {
                return candidate;
            }
        }
    }

    // Check relative to extension install path (bundled with the repo)
    const repoModules = path.resolve(extensionPath, '..', 'modules');
    if (fs.existsSync(repoModules)) {
        return repoModules;
    }

    return null;
}

function loadRulesFromDir(modulesDir: string): void {
    const config = vscode.workspace.getConfiguration('ukGovStandards');

    try {
        const entries = fs.readdirSync(modulesDir, { withFileTypes: true });
        for (const entry of entries) {
            if (!entry.isDirectory()) continue;

            const moduleName = entry.name;
            const moduleEnabled = config.get<boolean>(`modules.${moduleName}`, true);
            if (!moduleEnabled) continue;

            const rulesFile = path.join(modulesDir, moduleName, 'rules.json');
            if (fs.existsSync(rulesFile)) {
                loadRulesFile(rulesFile);
            }
        }
    } catch {
        // modules directory not readable — fall through to hardcoded checks
    }
}

function loadRulesFile(filePath: string): void {
    try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const data: RulesFile = JSON.parse(content);
        if (data.rules && Array.isArray(data.rules)) {
            loadedRules.push(...data.rules);
        }
    } catch {
        // invalid rules.json — skip silently
    }
}

export function runRuleEngine(document: vscode.TextDocument): CheckResult[] {
    if (loadedRules.length === 0) {
        return [];
    }

    const filePath = document.uri.fsPath;
    const relativePath = vscode.workspace.asRelativePath(filePath);
    const results: CheckResult[] = [];

    for (const rule of loadedRules) {
        if (!matchesGlob(relativePath, rule.filePattern)) {
            continue;
        }
        if (rule.excludeFilePattern && matchesGlob(relativePath, rule.excludeFilePattern)) {
            continue;
        }

        const regex = new RegExp(rule.pattern, 'gi');
        const excludeRegex = rule.excludePattern ? new RegExp(rule.excludePattern) : null;

        const text = document.getText();
        const lines = text.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            if (excludeRegex && excludeRegex.test(line)) {
                continue;
            }

            regex.lastIndex = 0;
            let match: RegExpExecArray | null;

            while ((match = regex.exec(line)) !== null) {
                const startPos = new vscode.Position(i, match.index);
                const endPos = new vscode.Position(i, match.index + match[0].length);

                const severity = rule.severity === 'error'
                    ? vscode.DiagnosticSeverity.Error
                    : rule.severity === 'warning'
                        ? vscode.DiagnosticSeverity.Warning
                        : vscode.DiagnosticSeverity.Information;

                const standardId = rule.id.split('-').slice(0, 2).join('-');

                results.push({
                    range: new vscode.Range(startPos, endPos),
                    message: rule.message,
                    severity,
                    standardId: rule.id,
                    standardUrl: `${REPO_URL}/blob/main/modules/core/standards/${standardId}.md`,
                });

                if (!regex.global) break;
            }
        }
    }

    return results;
}

function matchesGlob(filePath: string, pattern: string): boolean {
    const regexPattern = pattern
        .replace(/\./g, '\\.')
        .replace(/\*\*/g, '{{GLOBSTAR}}')
        .replace(/\*/g, '[^/]*')
        .replace(/\{\{GLOBSTAR\}\}/g, '.*')
        .replace(/\{([^}]+)\}/g, (_, choices) => `(${choices.split(',').join('|')})`);

    return new RegExp(`^${regexPattern}$`).test(filePath);
}

export function getRuleCount(): number {
    return loadedRules.length;
}
