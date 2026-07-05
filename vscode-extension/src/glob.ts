/**
 * Pure glob-to-regex matching — no VS Code dependency.
 * Extracted so it can be unit tested without the vscode module.
 */

export function matchesGlob(filePath: string, pattern: string): boolean {
    const regex = globToRegex(pattern);
    return regex.test(filePath);
}

export function globToRegex(pattern: string): RegExp {
    let regexStr = '';
    let i = 0;

    while (i < pattern.length) {
        const ch = pattern[i];

        if (ch === '\\') {
            i++;
            if (i < pattern.length) {
                regexStr += escapeRegexChar(pattern[i]);
            }
        } else if (ch === '*') {
            if (i + 1 < pattern.length && pattern[i + 1] === '*') {
                i++;
                if (i + 1 < pattern.length && pattern[i + 1] === '/') {
                    i++;
                }
                regexStr += '(?:.+/)?';
            } else {
                regexStr += '[^/]*';
            }
        } else if (ch === '?') {
            regexStr += '[^/]';
        } else if (ch === '{') {
            const closeIdx = pattern.indexOf('}', i);
            if (closeIdx === -1) {
                regexStr += '\\{';
            } else {
                const braceContent = pattern.substring(i + 1, closeIdx);
                const alternatives = splitBraceAlternatives(braceContent);
                const altRegexes = alternatives.map(alt => globToRegex(alt).source.slice(1, -1));
                regexStr += '(?:' + altRegexes.join('|') + ')';
                i = closeIdx;
            }
        } else if (ch === '[') {
            const closeIdx = pattern.indexOf(']', i + 1);
            if (closeIdx === -1) {
                regexStr += '\\[';
            } else {
                regexStr += pattern.substring(i, closeIdx + 1);
                i = closeIdx;
            }
        } else {
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
