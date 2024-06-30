const { DB_API_URL } = require('../../../config.json');
const { MAL_GRAPH_FP } = require('../../../config.json');
const { SlashCommandBuilder } = require('discord.js');


const data = new SlashCommandBuilder()
    .setName('mal_graph')
    .setDescription('get')
    .addStringOption(option =>
        option.setName('category')
            .setDescription('Anime or Manga')
            .setRequired(true)
            .addChoices(
                { name: 'Anime', value: 'anime' },
                { name: 'Manga', value: 'manga' }
            ))
        
	.addStringOption(option =>
		option.setName('title')
			.setDescription('Enter title of the anime/manga')
            .setRequired(true))  

    .addStringOption(option =>
        option.setName('type')
            .setDescription('Only required for anime')
            .setRequired(false)
            .addChoices(
                { name: 'All', value: 'all' },
                { name: 'TV', value: 'tv' },
                { name: 'Movie', value: 'movie' },
                { name: 'OVA', value: 'ova' },
                { name: 'ONA', value: 'ona' },
                { name: 'TV Special', value: 'tv_special' }
            ))

const execute = async (interaction) => {
    var category = interaction.options.getString('category');
    var title = interaction.options.getString('title');
    var type = interaction.options.getString('type');
    var msg = "";

    await interaction.deferReply()

    fetch(`${DB_API_URL}/mal/graph/${category}/${type}/${title}`)
        .then(response => {
            if (!response.ok) {
                console.log(response.json());
                throw new Error('Network response was not ok ' + response.statusText);
            }
            
            return response.json();
        })

        .then(async data => {          
            if ("error" in data) {
                await interaction.editReply(data['error']);
            } else {
                if (category == 'anime') {
                    msg = `- Completed: ${data['completed']}\n` +
                    `- Watching: ${data['watching']}\n` +
                    `- On Hold: ${data['on_hold']}\n` +
                    `- Dropped: ${data['dropped']}\n` +
                    `- Total: ${data['total']}`;
                } else {
                    msg = `- Completed: ${data['completed']}\n` +
                    `- Reading: ${data['reading']}\n` +
                    `- On Hold: ${data['on_hold']}\n` +
                    `- Dropped: ${data['dropped']}\n` +
                    `- Total: ${data['total']}`;
                }

                await interaction.editReply({ content: msg, files: [MAL_GRAPH_FP] });
            }
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

module.exports = {
	data: data,
	execute
};
