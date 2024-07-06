const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { DB_API_URL } = require('../../config.json');

const data = new SlashCommandBuilder()
    .setName('chairmen')
    .setDescription('Current chairmen for the rickies')

const execute = async (interaction) => {

    await interaction.deferReply()

    fetch(`${DB_API_URL}/connected`)
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
            const embed = new EmbedBuilder()
                .setColor(0x0099FF)
                .setTitle(data['title'])
                .setURL(data['url'])
                .setThumbnail('https://relayfm.s3.amazonaws.com/uploads/broadcast/image_3x/5/connected_artwork_0ecdaa3e-7019-4a34-86f7-f82d6a997144.png')
                .setDescription('Current chairmen for the rickies')
                .addFields(data['fields']);
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
