const lib = require('../../python_calls');
const { COMMANDS_FP } = require('../../config.json');
const { SlashCommandBuilder } = require('discord.js');


const data = new SlashCommandBuilder()
    .setName('graph')
    .setDescription('MMR graph over time')
	.addStringOption(option =>
		option.setName('in_game_names')
			.setDescription('First part of the username (no #), separated by commas')
			.setRequired(true))

const execute = async (interaction) => {
	var ign_list = interaction.options.getString('in_game_names');

    console.error('input: ', ign_list);
    await interaction.deferReply().catch(() => console.log("wow"))

    lib.python_calls([COMMANDS_FP, 'graph', ign_list])
        .then(async (result) => {

            const data = JSON.parse(result);

            if ("error" in data) {
                await interaction.editReply(data.error);
            } else {
                await interaction.editReply({ content: data.content, files: [data.filepath] });
            }
                
        })
        .catch(async (error) => {
            console.error('Error running Python process:', error);
            await interaction.editReply("Something went wrong");
        });
}

module.exports = {
	data: data,
	execute
}
