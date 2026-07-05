import * as vscode from 'vscode';
import * as diagnostics from './diagnostics';

export function activate(context: vscode.ExtensionContext): void {
    diagnostics.activate(context);

    const outputChannel = vscode.window.createOutputChannel('UK Gov Standards');
    outputChannel.appendLine('UK Gov Engineering Standards extension activated');
    context.subscriptions.push(outputChannel);
}

export function deactivate(): void {
    diagnostics.deactivate();
}
