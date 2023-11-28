const { SlashCommandBuilder } = require('discord.js');
const lib = require('../../python_calls');
const { COMMANDS_FP } = require('../../config.json');

const data = new SlashCommandBuilder()
    .setName('leaderboard')
    .setDescription('Valorant Leaderboards')
	.addStringOption(option =>
		option.setName('region')
			.setDescription('Region of the leaderboard')
			.setRequired(true)
			.addChoices(
				{ name: 'Asia Pacific', value: 'ap' },
				{ name: 'Europe', value: 'eu' },
				{ name: 'North America', value: 'na' },
				{ name: 'Local', value: 'local' },
			))

    .addStringOption(option =>
        option.setName('update')
            .setDescription('Latest data vs up to day old (for local)')
            .setRequired(false)
			.addChoices(
				{ name: 'True', value: 'true' },
				{ name: 'False', value: 'false' }
			));

const execute = async (interaction) => {
	var region = interaction.options.getString('region');
	var update = interaction.options.getString('update');

    await interaction.deferReply()

    lib.python_calls([COMMANDS_FP, 'leaderboard', region, update])
        .then(async (result) => {
            await interaction.editReply('```' + result + '```');
        })
        .catch((error) => {
            console.error('Error running Python process:', error);
        });
}

module.exports = {
	data: data,
	execute
}
