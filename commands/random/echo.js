const { SlashCommandBuilder } = require('discord.js');

const data = new SlashCommandBuilder()
	.setName('echo')
	.setDescription('Replies with your input!')
	.addStringOption(option =>
		option.setName('input')
			.setDescription('The input to echo back'))
	.addBooleanOption(option =>
		option.setName('ephemeral')
			.setDescription('Whether or not the echo should be ephemeral'));

async function execute(interaction) {
	var inp = interaction.options.getString('input');
	console.log(inp);
	await interaction.reply(inp);
}

module.exports = {
	data: data,
	execute
}