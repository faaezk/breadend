import random

sidearm = ["Classic", "Shorty", "Frenzy", "Ghost", "Sheriff"]
SMG = ["Stinger", "Spectre"]
Shotgun = ["Bucky"]
Rifle = ["Bulldog", "Guardian", "Phantom", "Vandal"]
Sniper = ["Marshal", "Operator"]
MG = ["Ares", "Odin"]
selected = random.choice([sidearm, SMG, Shotgun, Rifle, Sniper, MG])

print(random.choice(selected))