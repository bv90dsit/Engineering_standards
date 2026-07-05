import * as vscode from 'vscode';
import { checkSec001 } from './checks/sec001';
import { checkSec003 } from './checks/sec003';
import { checkWorkspace } from './checks/workspace';
import { loadRules, runRuleEngine, getRuleCount } from './rule-engine';
import { CheckResult } from './types';

let diagnosticCollection: vscode.DiagnosticCollection;
let workspaceDiagnosticCollection: vscode.DiagnosticCollection;
let debounceTimer: NodeJS.Timeout | undefined;
let workspaceChecked = false;
let useRuleEngine = false;

export function activate(context: vscode.ExtensionContext): void {
    diagnosticCollection = vscode.languages.createDiagnosticCollection('uk-gov-standards');
    workspaceDiagnosticCollection = vscode.languages.createDiagnosticCollection('uk-gov-standards-workspace');

    context.subscriptions.push(diagnosticCollection);
    context.subscriptions.push(workspaceDiagnosticCollection);

    // Load rules from modules
    loadRules(context.extensionPath);
    useRuleEngine = getRuleCount() > 0;

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            scheduleCheck(event.document);
        })
    );

    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(document => {
            runFileChecks(document);
        })
    );

    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(document => {
            runFileChecks(document);
            if (!workspaceChecked) {
                runWorkspaceChecks(document.uri);
                workspaceChecked = true;
            }
        })
    );

    context.subscriptions.push(
        vscode.workspace.onDidCloseTextDocument(document => {
            diagnosticCollection.delete(document.uri);
        })
    );

    if (vscode.window.activeTextEditor) {
        runFileChecks(vscode.window.activeTextEditor.document);
        runWorkspaceChecks(vscode.window.activeTextEditor.document.uri);
        workspaceChecked = true;
    }
}

function scheduleCheck(document: vscode.TextDocument): void {
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    debounceTimer = setTimeout(() => runFileChecks(document), 500);
}

function runFileChecks(document: vscode.TextDocument): void {
    const config = vscode.workspace.getConfiguration('ukGovStandards');

    if (!config.get<boolean>('enable', true)) {
        diagnosticCollection.clear();
        return;
    }

    if (document.uri.scheme !== 'file') {
        return;
    }

    let results: CheckResult[];

    if (useRuleEngine) {
        // Module-based: rules.json drives the checks
        results = runRuleEngine(document);
    } else {
        // Fallback: hardcoded checks (standalone install without modules)
        results = [];
        if (config.get<boolean>('checks.sec001', true)) {
            results.push(...checkSec001(document));
        }
        if (config.get<boolean>('checks.sec003', true)) {
            results.push(...checkSec003(document));
        }
    }

    const diagnostics = results.map(result => {
        const diagnostic = new vscode.Diagnostic(
            result.range,
            result.message,
            result.severity
        );
        diagnostic.source = 'UK Gov Standards';
        diagnostic.code = {
            value: result.standardId,
            target: vscode.Uri.parse(result.standardUrl),
        };
        return diagnostic;
    });

    diagnosticCollection.set(document.uri, diagnostics);
}

async function runWorkspaceChecks(triggerUri: vscode.Uri): Promise<void> {
    const config = vscode.workspace.getConfiguration('ukGovStandards');

    if (!config.get<boolean>('enable', true)) {
        return;
    }

    const results = await checkWorkspace();

    if (results.length === 0) {
        return;
    }

    const diagnostics = results.map(result => {
        const diagnostic = new vscode.Diagnostic(
            new vscode.Range(0, 0, 0, 0),
            result.message,
            vscode.DiagnosticSeverity.Information
        );
        diagnostic.source = 'UK Gov Standards';
        diagnostic.code = {
            value: result.standardId,
            target: vscode.Uri.parse(result.standardUrl),
        };
        return diagnostic;
    });

    workspaceDiagnosticCollection.set(triggerUri, diagnostics);
}

export function deactivate(): void {
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
}
