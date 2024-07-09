import requests

def test(url):
    r = requests.get(url)
    print(r.text)

# LEADERBOARD
# test("http://127.0.0.1:5000/valorant/leaderboard/ap")
# test("http://127.0.0.1:5000/valorant/leaderboard/eu")
# test("http://127.0.0.1:5000/valorant/leaderboard/kr")
# test("http://127.0.0.1:5000/valorant/leaderboard/na")
# test("http://127.0.0.1:5000/valorant/leaderboard/local")
# test("http://127.0.0.1:5000/valorant/leaderboard/local/true")

# STATS
test("http://127.0.0.1:5000/valorant/stats/fakinator")
# test("http://127.0.0.1:5000/valorant/stats/fakinator/4269")
# test("http://127.0.0.1:5000/valorant/stats/fakinat")
# test("http://127.0.0.1:5000/valorant/stats/fakinator/4444")

# BANNER
# test("http://127.0.0.1:5000/valorant/banner/fakinator")
# test("http://127.0.0.1:5000/valorant/banner/fakinator/4269")
# test("http://127.0.0.1:5000/valorant/banner/fakinat")
# test("http://127.0.0.1:5000/valorant/banner/fakinator/4444")

# GRAPH
# test("http://127.0.0.1:5000/valorant/graph/fakinator,dilka30003")
# test("http://127.0.0.1:5000/valorant/graph/fakinator,dilka303")
# test("http://127.0.0.1:5000/valorant/graph/fakinat,dilka303")
# test("http://127.0.0.1:5000/valorant/graph/fakinat")

#ANIME SEARCH
test("http://127.0.0.1:5000/mal/info/anime/tv/one piece")
test("http://127.0.0.1:5000/mal/info/anime/movie/one piece")
test("http://127.0.0.1:5000/mal/info/anime/ova/one piece")
test("http://127.0.0.1:5000/mal/info/anime/special/one piece")
test("http://127.0.0.1:5000/mal/info/anime/ona/one piece")
test("http://127.0.0.1:5000/mal/info/anime/music/one piece")
test("http://127.0.0.1:5000/mal/info/anime/cm/one piece")
test("http://127.0.0.1:5000/mal/info/anime/pv/one piece")
test("http://127.0.0.1:5000/mal/info/anime/tv_special/dr. stone")
test("http://127.0.0.1:5000/mal/info/anime/ff/fdf")

# MANGA SEARCH
test("http://127.0.0.1:5000/mal/info/manga/jujutsu kaisen")
test("http://127.0.0.1:5000/mal/info/manga/")

# CHARACTER SEARCH
test("http://127.0.0.1:5000/mal/info/character/hinata shoyo")
test("http://127.0.0.1:5000/mal/info/character/")

#MAL GRAPHS
test("http://127.0.0.1:5000/mal/graph/anime/tv/one piece")
test("http://127.0.0.1:5000/mal/graph/manga/one piece")
test("http://127.0.0.1:5000/mal/graph/anime/one piece")

# CONNECTED
test("http://127.0.0.1:5000/other/connected")
