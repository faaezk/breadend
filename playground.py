from jikanpy import Jikan

def animestuff(name):
	jikan = Jikan()
	search_result = jikan.search('anime', name)
	id = search_result['results'][0]['mal_id']
	anime = jikan.anime(id)
	url = anime['url']
	image = anime['image_url']
	OP = anime['opening_themes']
	return [url, image, OP]

print(animestuff("yuru camp"))
