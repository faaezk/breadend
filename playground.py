from jikanpy import Jikan

def animestuff(name):

	jikan = Jikan()
	search_result = jikan.search('anime', name, page=1)

	id = search_result['results'][0]['mal_id']


	anime = jikan.anime(id)

	title = anime['title']
	url = anime['url']
	image = anime['image_url']

	source = anime['source']
	score = anime['score']

	ep_count = anime['episodes']
	dates = anime['aired']['string']

	OP = anime['opening_themes']
	ending_themes = anime['ending_themes']

	sequel = ""
	if 'Sequel' in anime['related'].keys():
		for x in anime['related']['Sequel']:
			sequel += x['name'] 

	genres = ""
	for genre in anime['genres']:
		genres += genre['name']

	return [title, source, ep_count, dates, score, OP, ending_themes, sequel, genres]

print(animestuff("hunter hunter 2011"))
