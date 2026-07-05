import * as assert from 'assert';
import { matchesGlob } from '../../glob';

suite('Glob Matching', () => {
    test('* matches filename', () => {
        assert.strictEqual(matchesGlob('file.py', '*.py'), true);
        assert.strictEqual(matchesGlob('file.ts', '*.py'), false);
    });

    test('* does not match path separators', () => {
        assert.strictEqual(matchesGlob('src/file.py', '*.py'), false);
    });

    test('** matches any depth', () => {
        assert.strictEqual(matchesGlob('src/components/Button.tsx', '**/*.tsx'), true);
        assert.strictEqual(matchesGlob('Button.tsx', '**/*.tsx'), true);
        assert.strictEqual(matchesGlob('deep/nested/path/file.tsx', '**/*.tsx'), true);
    });

    test('** with directory prefix', () => {
        assert.strictEqual(matchesGlob('src/app.ts', 'src/**/*.ts'), true);
        assert.strictEqual(matchesGlob('src/deep/app.ts', 'src/**/*.ts'), true);
        assert.strictEqual(matchesGlob('other/app.ts', 'src/**/*.ts'), false);
    });

    test('brace expansion {a,b}', () => {
        assert.strictEqual(matchesGlob('file.ts', '*.{ts,tsx}'), true);
        assert.strictEqual(matchesGlob('file.tsx', '*.{ts,tsx}'), true);
        assert.strictEqual(matchesGlob('file.js', '*.{ts,tsx}'), false);
    });

    test('brace expansion in path', () => {
        assert.strictEqual(matchesGlob('src/file.ts', '**/*.{ts,tsx}'), true);
        assert.strictEqual(matchesGlob('src/file.tsx', '**/*.{ts,tsx}'), true);
        assert.strictEqual(matchesGlob('src/file.py', '**/*.{ts,tsx}'), false);
    });

    test('? matches single character', () => {
        assert.strictEqual(matchesGlob('file1.py', 'file?.py'), true);
        assert.strictEqual(matchesGlob('file12.py', 'file?.py'), false);
    });

    test('dots are escaped', () => {
        assert.strictEqual(matchesGlob('file.py', '*.py'), true);
        assert.strictEqual(matchesGlob('filexpy', '*.py'), false);
    });

    test('exclude patterns from rules.json', () => {
        assert.strictEqual(matchesGlob('src/app.test.ts', '**/*.test.*'), true);
        assert.strictEqual(matchesGlob('src/app.spec.ts', '**/*.spec.*'), true);
        assert.strictEqual(matchesGlob('src/app.ts', '**/*.test.*'), false);
    });

    test('real-world patterns from rules.json', () => {
        assert.strictEqual(matchesGlob('src/api.py', '**/*.{py,js,ts,go,java,rb}'), true);
        assert.strictEqual(matchesGlob('deep/path/file.java', '**/*.{py,js,ts,go,java,rb}'), true);
        assert.strictEqual(matchesGlob('README.md', '**/*.{py,js,ts,go,java,rb}'), false);
    });

    test('test file exclusion patterns', () => {
        assert.strictEqual(matchesGlob('test_views.py', '**/test_*'), true);
        assert.strictEqual(matchesGlob('src/test_views.py', '**/test_*'), true);
    });

    test('tsconfig pattern', () => {
        assert.strictEqual(matchesGlob('tsconfig.json', '**/tsconfig*.json'), true);
        assert.strictEqual(matchesGlob('packages/web/tsconfig.build.json', '**/tsconfig*.json'), true);
    });
});
