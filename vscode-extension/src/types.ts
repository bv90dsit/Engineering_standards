import * as vscode from 'vscode';

export interface CheckResult {
    range: vscode.Range;
    message: string;
    severity: vscode.DiagnosticSeverity;
    standardId: string;
    standardUrl: string;
}

export const REPO_URL = 'https://github.com/bv90dsit/Engineering_standards';

export function standardUrl(id: string): string {
    return `${REPO_URL}/blob/main/standards/${id}.md`;
}
