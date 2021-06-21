
class player:
    def __init__(self, ign, tag, name, online):
        self.ign = ign
        self.tag = tag
        self.name = name
        self.online = online

classyplayers = [
    
    player("silentwhispers", "0000", "Rasindu", True),
    player("fakinator", "4269", "Faaez", True),
    player("faqinator", "7895", "Faaez alt", False),
    player("8888", "nadi", "Hadi", True),
    player("dilka30003", "0000", "Dhiluka", True),
    player("slumonaire", "oce", "Chris", True),
    player("katchampion", "oce", "Albert", False),
    player("imabandwagon", "oce", "Dylan", True),
    player("giroud", "8383", "Dylan alt", False),
    player("oshaoshawott", "oce", "Osha", False),
    player("yovivels", "1830", "Viv", False),
    player("therealrobdez", "3333", "Will", False),
    player("bento2", "box", "Ben alt", False),
    player("hoben222", "9327", "Ben", True),
    player("jokii", "oce", "Henry", False),
    player("lyçhii", "mai", "Bog", False),
    player("lmao", "6548", "Joseph lmao", True),
    player("jack", "ytb", "Jack", False),
    player("vkj", "4084", "Rasindu alt", False),
    player("tallewok", "6209", "Rasindu alt 2", False),
    player("fade", "1280", "Rasindu gold smurf", False),
    player("skzcross", "oce", "Bhairav", False),
    player("lol", "1280", "Joseph lol", False),
    player("crossaxis", "mippl", "Josh", False),
    player("azatory", "nike", "Alex", False),
    player("quyteriyaki", "oce", "James", False),
    player("talizorahrayya", "3303", "worst child", False),
    player("quackinator", "2197", "Faaez smurf", False)
    ]

players = [("silentwhispers", "0000"), 
    ("fakinator", "4269"), 
    ("faqinator", "7895"), 
    ("8888", "nadi"), 
    ("dilka30003", "0000"),
    ("slumonaire", "oce"),
    ("katchampion", "oce"), 
    ("imabandwagon", "oce"), 
    ("giroud", "8383"), 
    ("oshaoshawott", "oce"), 
    ("yovivels", "1830"), 
    ("therealrobdez", "3333"),
    ("bento2", "box"), 
    ("hoben222", "9327"), 
    ("jokii", "oce"),
    ("lyçhii", "mai"),
    ("lmao", "6548"),
    ("jack", "ytb"),
    ("vkj", "4084"),
    ("tallewok", "6209"),
    ("fade", "1280"),
    ("skzcross", "oce"),
    ("lol", "4529"),
    ("crossaxis", "mippl"),
    ("azatory", "nike"),
    ("quyteriyaki", "oce"), 
    ("talizorahrayya", "3303"), 
    ("quackinator", "2197")
    ]

online_players = [ 
    ["fakinator", "4269"],
    ["8888", "nadi"], 
    ["dilka30003", "0000"],
    ["slumonaire", "oce"],
    ["hoben222", "9327"],
    ["silentwhispers", "0000"],
    ["imabandwagon", "oce"],
    ["lmao", "6548"]
    ]

names = {"fakinator" : "Faaez", "8888" : "Hadi", "dilka30003" : "Dhiluka", 
        "slumonaire" : "Chris", "hoben222" : "Ben", "silentwhispers" : "Rasindu",
        "imabandwagon" : "Dylan", "lmao" : "Joseph"}

game_names = {"Faaez" : "fakinator", "Hadi" : "8888", "Dhiluka" : "dilka30003", 
        "Chris" : "slumonaire", "Ben" : "hoben222", "Rasindu" : "silentwhispers",
        "Dylan" : "imabandwagon", "Joseph" : "lmao"}

def get_attribute(value, attribute):

    if attribute == "ign":

        for player in classyplayers:
            if player.name == value:
                return player.ign

    if attribute == "name":

        for player in classyplayers:
            if player.ign == value:
                return player.name