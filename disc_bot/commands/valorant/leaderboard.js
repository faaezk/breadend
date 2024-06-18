const { SlashCommandBuilder } = require('discord.js');
const { DB_API_URL } = require('../config.json');

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

	fetch(`${DB_API_URL}/valorant/leaderboard/${region}/${update}`)
		.then(response => {
			if (!response.ok) {
				console.log(response.json());
				throw new Error('Network response was not ok ' + response.statusText);
			}
			
			return response.json();
		})

		.then(async data => {
			console.log(data); // Handle the data from the response
			await interaction.editReply('```' + data['title'] + '\n' + data['leaderboard'] + '```');
		})
		.catch(error => {
			console.error('There was a problem with the fetch operation:', error);
		});
}

module.exports = {
	data: data,
	execute
}
