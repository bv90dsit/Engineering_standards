import * as path from 'path';
import Mocha from 'mocha';
import * as fs from 'fs';

export function run(): Promise<void> {
    const mocha = new Mocha({ ui: 'tdd', color: true });
    const testsRoot = __dirname;

    return new Promise((resolve, reject) => {
        const files = fs.readdirSync(testsRoot).filter(f => f.endsWith('.test.js'));
        files.forEach(f => mocha.addFile(path.resolve(testsRoot, f)));

        try {
            mocha.run(failures => {
                if (failures > 0) {
                    reject(new Error(`${failures} tests failed.`));
                } else {
                    resolve();
                }
            });
        } catch (err) {
            reject(err);
        }
    });
}
