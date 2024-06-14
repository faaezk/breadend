function python_calls(args) {
    return new Promise((resolve, reject) => {
        const spawner = require('child_process').spawn;
        const python_process = spawner('python3', args);;

        let stdoutData = '';
        let stderrData = '';

        python_process.stdout.on('data', (data) => {
            stdoutData += data.toString();
        });

        python_process.stderr.on('data', (data) => {
            stderrData += data.toString();
        });

        python_process.on('error', (err) => {
            reject(err);
        });

        python_process.on('close', (code) => {
            if (code === 0) {
                resolve(stdoutData);
            } else {
                reject(`Python process exited with code ${code}. Error: ${stderrData}`);
            }
        });
    });
}

module.exports = { python_calls };