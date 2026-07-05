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
let outputCh: vscode.OutputChannel | undefined;

export function loadRules(extensionPath: string, outputChannel?: vscode.OutputChannel): void {
    loadedRules = [];
    outputCh = outputChannel;

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
    } catch (error) {
        if (outputCh) {
            outputCh.appendLine(`[UK Gov Standards] Warning: Failed to load rules from modules directory: ${error}`);
        }
    }
}

function loadRulesFile(filePath: string): void {
    try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const data: RulesFile = JSON.parse(content);
        if (data.rules && Array.isArray(data.rules)) {
            loadedRules.push(...data.rules);
        }
    } catch (error) {
        if (outputCh) {
            const name = path.basename(path.dirname(filePath));
            outputCh.appendLine(`[UK Gov Standards] Warning: Failed to load rules from modules/${name}/rules.json: ${error}`);
        }
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
    const regex = globToRegex(pattern);
    return regex.test(filePath);
}

function globToRegex(pattern: string): RegExp {
    let regexStr = '';
    let i = 0;

    while (i < pattern.length) {
        const ch = pattern[i];

        if (ch === '\\') {
            // Escaped character — take next char literally (regex-escaped)
            i++;
            if (i < pattern.length) {
                regexStr += escapeRegexChar(pattern[i]);
            }
        } else if (ch === '*') {
            if (i + 1 < pattern.length && pattern[i + 1] === '*') {
                // Globstar **
                i++; // consume second *
                // ** may be surrounded by slashes: consume a trailing slash if present
                if (i + 1 < pattern.length && pattern[i + 1] === '/') {
                    i++; // consume trailing /
                }
                // Match any path depth (zero or more path segments)
                regexStr += '(?:.+/)?';
            } else {
                // Single * — match anything except /
                regexStr += '[^/]*';
            }
        } else if (ch === '?') {
            // Match any single character except /
            regexStr += '[^/]';
        } else if (ch === '{') {
            // Brace expansion: {a,b,c}
            const closeIdx = pattern.indexOf('}', i);
            if (closeIdx === -1) {
                // No closing brace — treat as literal
                regexStr += '\\{';
            } else {
                const braceContent = pattern.substring(i + 1, closeIdx);
                const alternatives = splitBraceAlternatives(braceContent);
                // Recursively convert each alternative (they may contain dots, wildcards, etc.)
                const altRegexes = alternatives.map(alt => globToRegex(alt).source.slice(1, -1)); // strip ^ and $
                regexStr += '(?:' + altRegexes.join('|') + ')';
                i = closeIdx; // will be incremented at end of loop
            }
        } else if (ch === '[') {
            // Character class — pass through to regex as-is until closing ]
            const closeIdx = pattern.indexOf(']', i + 1);
            if (closeIdx === -1) {
                regexStr += '\\[';
            } else {
                regexStr += pattern.substring(i, closeIdx + 1);
                i = closeIdx;
            }
        } else {
            // Literal character — escape regex metacharacters
            regexStr += escapeRegexChar(ch);
        }

        i++;
    }

    return new RegExp('^' + regexStr + '$');
}

function escapeRegexChar(ch: string): string {
    if ('.+^${}()|[]\\/?*'.indexOf(ch) !== -1) {
        return '\\' + ch;
    }
    return ch;
}

function splitBraceAlternatives(content: string): string[] {
    // Split on commas, but respect nested braces
    const parts: string[] = [];
    let depth = 0;
    let current = '';

    for (const ch of content) {
        if (ch === '{') {
            depth++;
            current += ch;
        } else if (ch === '}') {
            depth--;
            current += ch;
        } else if (ch === ',' && depth === 0) {
            parts.push(current);
            current = '';
        } else {
            current += ch;
        }
    }
    parts.push(current);
    return parts;
}

export function getRuleCount(): number {
    return loadedRules.length;
}
