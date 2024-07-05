const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Replies with Pong!'),
		
	async execute(interaction) {
		const exampleEmbed = new EmbedBuilder()
			.setTitle('Poing')
			.setDescription('ping pong')

		await interaction.reply({
			content: "pong",
			embeds: [exampleEmbed]
		});
	},
};
