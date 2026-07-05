import * as vscode from 'vscode';
import { CheckResult, standardUrl } from '../types';

const HTTP_PATTERN = /http:\/\/(?!localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])/g;

const EXCLUDED_EXTENSIONS = new Set(['.md', '.txt', '.rst', '.adoc']);

export function checkSec001(document: vscode.TextDocument): CheckResult[] {
    const ext = document.fileName.substring(document.fileName.lastIndexOf('.'));
    if (EXCLUDED_EXTENSIONS.has(ext)) {
        return [];
    }

    if (document.fileName.includes('.test.') || document.fileName.includes('.spec.')) {
        return [];
    }

    const results: CheckResult[] = [];
    const text = document.getText();
    const lines = text.split('\n');

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        if (trimmed.startsWith('//') || trimmed.startsWith('#') || trimmed.startsWith('*')) {
            continue;
        }

        let match: RegExpExecArray | null;
        HTTP_PATTERN.lastIndex = 0;

        while ((match = HTTP_PATTERN.exec(line)) !== null) {
            const startPos = new vscode.Position(i, match.index);
            const endPos = new vscode.Position(i, match.index + match[0].length);

            results.push({
                range: new vscode.Range(startPos, endPos),
                message: `SEC-001: Use HTTPS instead of HTTP. All connections must use TLS.`,
                severity: vscode.DiagnosticSeverity.Warning,
                standardId: 'SEC-001',
                standardUrl: standardUrl('SEC-001'),
            });
        }
    }

    return results;
}
