const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { DB_API_URL } = require('../../config.json');

const data = new SlashCommandBuilder()
    .setName('stats')
    .setDescription('Ranked statistics for all acts')
	.addStringOption(option =>
		option.setName('ign')
			.setDescription('First part of the username (no #)')
			.setRequired(true))

    .addStringOption(option =>
        option.setName('tag')
            .setDescription('Second part of the username (no #)')
            .setRequired(false));

const execute = async (interaction) => {
	var ign = interaction.options.getString('ign');
	var tag = interaction.options.getString('tag');
    if (!tag) {
        tag = "emptytag"
    }

    await interaction.deferReply()
    
    fetch(`${DB_API_URL}/valorant/stats/${ign}/${tag}`)
    .then(response => {
        if (!response.ok) {
            console.log(response.json());
            throw new Error('Network response was not ok ' + response.statusText);
        }
        
        return response.json();
    })

    .then(async data => {
        if ("error" in data) {
            await interaction.editReply(data.error);
        } else {
            const updatedFields = data['fields'].map(item => ({ ...item, inline: true }));
            const embed = new EmbedBuilder()
                .setColor(0x0099FF)
                .setTitle(data['title'])
                .setAuthor({ name: data['author'], iconURL: data['thumbnail'], url: data['url']})
                .addFields(updatedFields);
            await interaction.editReply({ content: "woah", embeds: [embed] });
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
