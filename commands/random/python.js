const { SlashCommandBuilder } = require('discord.js');
const { ABS_FP } = require('../../config.json');

const data = new SlashCommandBuilder()
    .setName('python')
    .setDescription('uses python')
	.addStringOption(option =>
		option.setName('input')
			.setDescription('The input to echo back'));


function python_stuff(inp) {
    return new Promise((resolve, reject) => {
        const spawner = require('child_process').spawn;
        const python_process = spawner('python3', [ABS_FP + '/test.py', inp]);

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
            

const execute = async (interaction) => {
	var inp = interaction.options.getString('input');
    console.log(inp);

    python_stuff(inp)
        .then(async (result) => {
            console.log('Python process output:', result);
            await interaction.reply(result);
        })
        .catch((error) => {
            console.error('Error running Python process:', error);
        });

    console.log(inp);
}

module.exports = {
	data: data,
	execute
}