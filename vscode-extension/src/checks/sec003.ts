import * as vscode from 'vscode';
import { CheckResult, standardUrl } from '../types';

const SECRET_PATTERNS: { pattern: RegExp; label: string }[] = [
    {
        pattern: /(password|passwd|pwd)\s*[=:]\s*['"][^'"]{8,}['"]/gi,
        label: 'hardcoded password',
    },
    {
        pattern: /(api_key|apikey|api_secret)\s*[=:]\s*['"][^'"]{8,}['"]/gi,
        label: 'hardcoded API key',
    },
    {
        pattern: /(secret|secret_key)\s*[=:]\s*['"][^'"]{8,}['"]/gi,
        label: 'hardcoded secret',
    },
    {
        pattern: /(token|auth_token|access_token)\s*[=:]\s*['"][^'"]{8,}['"]/gi,
        label: 'hardcoded token',
    },
    {
        pattern: /(private_key)\s*[=:]\s*['"][^'"]{8,}['"]/gi,
        label: 'hardcoded private key',
    },
    {
        pattern: /AKIA[0-9A-Z]{16}/g,
        label: 'AWS access key',
    },
];

const EXCLUDED_PATTERNS = ['.example', '.sample', '.template', '.env.example'];

export function checkSec003(document: vscode.TextDocument): CheckResult[] {
    const fileName = document.fileName;

    if (EXCLUDED_PATTERNS.some(p => fileName.includes(p))) {
        return [];
    }
    if (fileName.includes('.test.') || fileName.includes('.spec.')) {
        return [];
    }

    const results: CheckResult[] = [];
    const text = document.getText();
    const lines = text.split('\n');

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        for (const { pattern, label } of SECRET_PATTERNS) {
            pattern.lastIndex = 0;
            let match: RegExpExecArray | null;

            while ((match = pattern.exec(line)) !== null) {
                const startPos = new vscode.Position(i, match.index);
                const endPos = new vscode.Position(i, match.index + match[0].length);

                results.push({
                    range: new vscode.Range(startPos, endPos),
                    message: `SEC-003: Possible ${label} detected. Secrets must not be committed to source code. Use environment variables or a secrets manager.`,
                    severity: vscode.DiagnosticSeverity.Error,
                    standardId: 'SEC-003',
                    standardUrl: standardUrl('SEC-003'),
                });
            }
        }
    }

    return results;
}
