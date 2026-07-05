import * as assert from 'assert';

suite('Rule Pattern Matching', () => {
    test('SEC-001: detects http:// URLs', () => {
        const pattern = /http:\/\/(?!localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])/g;
        assert.strictEqual(pattern.test('const url = "http://example.com"'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('const url = "http://localhost:3000"'), false);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('const url = "https://example.com"'), false);
    });

    test('SEC-003: detects hardcoded passwords', () => {
        const pattern = /(password|passwd|pwd)\s*[=:]\s*['"][^'"]{8,}['"]/gi;
        assert.strictEqual(pattern.test('password = "supersecret123"'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('password = os.environ["DB_PASS"]'), false);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('pwd = "short"'), false);
    });

    test('SEC-003: detects AWS keys', () => {
        const pattern = /AKIA[0-9A-Z]{16}/g;
        assert.strictEqual(pattern.test('aws_key = "AKIAIOSFODNN7EXAMPLE"'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('some_other_string'), false);
    });

    test('PY-001: detects print()', () => {
        const pattern = /\bprint\s*\(/g;
        assert.strictEqual(pattern.test('print("hello")'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('  print(f"debug: {x}")'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('fingerprint = get_hash()'), false);
    });

    test('PY-004: detects wildcard imports', () => {
        const pattern = /^from\s+\S+\s+import\s+\*/;
        assert.strictEqual(pattern.test('from os import *'), true);
        assert.strictEqual(pattern.test('from django.conf import settings'), false);
        assert.strictEqual(pattern.test('import os'), false);
    });

    test('JV-002: detects System.out.println', () => {
        const pattern = /System\.(out|err)\.(print|println)/g;
        assert.strictEqual(pattern.test('System.out.println("debug")'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('System.err.print("error")'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('logger.info("correct")'), false);
    });

    test('TS-002: detects any type', () => {
        const pattern = /:\s*any\b/g;
        assert.strictEqual(pattern.test('const x: any = {}'), true);
        pattern.lastIndex = 0;
        assert.strictEqual(pattern.test('const x: string = "hello"'), false);
    });

    test('exclude patterns skip comments', () => {
        const excludePattern = /^\s*(#|\/\/|\*)/;
        assert.strictEqual(excludePattern.test('# this is a comment'), true);
        assert.strictEqual(excludePattern.test('// this is a comment'), true);
        assert.strictEqual(excludePattern.test('* javadoc line'), true);
        assert.strictEqual(excludePattern.test('code here'), false);
        assert.strictEqual(excludePattern.test('  # indented comment'), true);
    });
});
