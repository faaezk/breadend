const { DB_API_URL } = require('../../../config.json');
const { SlashCommandBuilder } = require('discord.js');


const data = new SlashCommandBuilder()
    .setName('banner')
    .setDescription('Shows a players banner')
	.addStringOption(option =>
		option.setName('username')
			.setDescription('enter username as ign#tag')
			.setRequired(true))

const execute = async (interaction) => {
    var username = interaction.options.getString('username');
    await interaction.deferReply()

    fetch(`${DB_API_URL}/valorant/banner/${username}`)
        .then(response => {
            if (!response.ok) {
                console.log(response.json());
                throw new Error('Network response was not ok ' + response.statusText);
            }
            
            return response.json();
        })

        .then(async data => {
            console.log(data); // Handle the data from the response
            
            if ("error" in data) {
                await interaction.editReply(data['error']);
            } else {
                await interaction.editReply({ content: data['content'], files: [data['filepath']] });
            }
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

module.exports = {
	data: data,
	execute
}
