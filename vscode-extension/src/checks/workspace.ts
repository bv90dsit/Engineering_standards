import * as vscode from 'vscode';
import { CheckResult, standardUrl } from '../types';

export interface WorkspaceCheckResult {
    message: string;
    standardId: string;
    standardUrl: string;
}

export async function checkWorkspace(): Promise<WorkspaceCheckResult[]> {
    const results: WorkspaceCheckResult[] = [];

    if (!vscode.workspace.workspaceFolders?.length) {
        return results;
    }

    const config = vscode.workspace.getConfiguration('ukGovStandards');

    if (config.get<boolean>('checks.eng001', true)) {
        const licence = await vscode.workspace.findFiles('{LICEN[CS]E*,licen[cs]e*}', null, 1);
        if (licence.length === 0) {
            results.push({
                message: 'ENG-001: No LICENCE file found. Add a LICENCE file (MIT or OGL v3) to the repository root.',
                standardId: 'ENG-001',
                standardUrl: standardUrl('ENG-001'),
            });
        }
    }

    if (config.get<boolean>('checks.sec002', true)) {
        const scanners = await vscode.workspace.findFiles(
            '{.github/dependabot.yml,.github/dependabot.yaml,.snyk,.trivyignore,renovate.json,.renovaterc}',
            null, 1
        );
        if (scanners.length === 0) {
            results.push({
                message: 'SEC-002: No dependency scanning configured. Add .github/dependabot.yml or equivalent.',
                standardId: 'SEC-002',
                standardUrl: standardUrl('SEC-002'),
            });
        }
    }

    if (config.get<boolean>('checks.eng003', true)) {
        const workflows = await vscode.workspace.findFiles(
            '{.github/workflows/*.yml,.github/workflows/*.yaml,.gitlab-ci.yml,Jenkinsfile}',
            null, 1
        );
        if (workflows.length === 0) {
            results.push({
                message: 'ENG-003: No CI configuration found. Add a workflow in .github/workflows/ with automated tests.',
                standardId: 'ENG-003',
                standardUrl: standardUrl('ENG-003'),
            });
        }
    }

    if (config.get<boolean>('checks.eng004', true)) {
        const readmes = await vscode.workspace.findFiles('{README.md,readme.md,README}', null, 1);
        if (readmes.length === 0) {
            results.push({
                message: 'ENG-004: No README found. Add a README.md explaining the service and how to get started.',
                standardId: 'ENG-004',
                standardUrl: standardUrl('ENG-004'),
            });
        } else {
            const doc = await vscode.workspace.openTextDocument(readmes[0]);
            if (doc.lineCount < 10) {
                results.push({
                    message: 'ENG-004: README exists but is very short (< 10 lines). A new joiner should be able to understand and run the service from the README.',
                    standardId: 'ENG-004',
                    standardUrl: standardUrl('ENG-004'),
                });
            }
        }
    }

    return results;
}
