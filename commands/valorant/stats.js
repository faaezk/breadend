const { SlashCommandBuilder } = require('discord.js');
const { EmbedBuilder } = require('discord.js');
const lib = require('../../python_calls');
const { COMMANDS_FP } = require('../../config.json');

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

    await interaction.deferReply()

    if (!tag) {
        tag = "emptytag"
    }

    lib.python_calls([COMMANDS_FP, 'stats', ign, tag])
        .then(async (result) => {
            const data = JSON.parse(result);

            if ("error" in data) {
                await interaction.editReply(data.error);
            } else {

                // Set fields to be in rows
                const updatedFields = data.fields.map(item => ({ ...item, inline: true }));
                const embed = new EmbedBuilder()
                    .setColor(0x0099FF)
                    .setTitle(data.title)
                    .setAuthor({ name: data.author, iconURL: data.thumbnail, url: data.url})
                    .addFields(updatedFields);
                await interaction.editReply({ embeds: [embed] });
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
