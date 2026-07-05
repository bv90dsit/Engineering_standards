import * as vscode from 'vscode';
import * as diagnostics from './diagnostics';

export function activate(context: vscode.ExtensionContext): void {
    const outputChannel = vscode.window.createOutputChannel('UK Gov Standards');
    outputChannel.appendLine('UK Gov Engineering Standards extension activated');
    context.subscriptions.push(outputChannel);

    diagnostics.activate(context, outputChannel);
}

export function deactivate(): void {
    diagnostics.deactivate();
}
