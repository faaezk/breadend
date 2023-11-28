const lib = require('../../python_calls');
const { COMMANDS_FP } = require('../../config.json');
const { SlashCommandBuilder } = require('discord.js');


const data = new SlashCommandBuilder()
    .setName('graph')
    .setDescription('MMR graph over time')
	.addStringOption(option =>
		option.setName('ign')
			.setDescription('First part of the username (no #)')
			.setRequired(true))

const execute = async (interaction) => {
	var ign = interaction.options.getString('ign');

    await interaction.deferReply()

    lib.python_calls([COMMANDS_FP, 'graph', ign])
        .then(async (result) => {

            const data = JSON.parse(result);

            if ("error" in data) {
                await interaction.editReply(data.error);
            } else {
                await interaction.editReply({ content: data.content, files: [data.filepath] });
            }
                
        })
        .catch((error) => {
            console.error('Error running Python process:', error);
        });
}

module.exports = {
	data: data,
	execute
}
