import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import os
import valorant
import playerclass
import math

ranks = {
0 : "Iron 1", 100 : "Iron 2", 200 : "Iron 3",
300 : "Bronze 1", 400 : "Bronze 2", 500 : "Bronze 3",
600 : "Silver 1", 700 : "Silver 2", 800 : "Silver 3",
900 : "Gold 1", 1000 : "Gold 2", 1100 : "Gold 3",
1200 : "Platinum 1", 1300 : "Platinum 2", 1400 : "Platinum 3",
1500 : "Diamond 1", 1600 : "Diamond 2", 1700 : "Diamond 3",
1800 : "Immortal"
}

def roundup(x):
  return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
  return int(math.floor(x / 100.0)) * 100

def make_graph(username):

  if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)) == False:
      return False
  
  playerlist = playerclass.PlayerList('playerlist.csv')
  playerlist.load()

  tagline = ""
  for player in playerlist.players:
      if player.ign == username:
          tagline = player.tag
          break

  valorant.update_elo_history(username, tagline)
  
  file1 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), 'r')

  y = [x.strip() for x in file1.readlines()]
  if len(y) == 2:
      return None
  y.pop(0)
  x = []

  for i in range(0, len(y)):
      y[i] = int(y[i])
      x.append(i + 1)

  ymin = rounddown(min(y))
  ymax = roundup(max(y))

  axes = plt.gca()
  axes.set_ylim([ymin,ymax])
  
  ticks = []
  i = int(math.floor(ymin / 50.0)) * 50

  ranger = int((ymax-ymin)/100)

  while i <= int(math.ceil(ymax / 50.0)) * 50:
      ticks.append(i)
      if ranger == 1:
          i += 20
      elif ranger > 4:
          i += 50
      else:
          i += 25

  axes.set_yticks(ticks)
  labely = []

  for value in ticks:
      if value % 100 != 0:
          labely.append(str(value))

      else:
          labely.append(ranks[value])

  tickx = []  
  i = 0
  j = 0

  if len(x) <= 15:
      j = 1
  elif len(x) > 15 and len(x) < 30:
      j = 2
  elif len(x) >= 30 and len(x) < 70:
      j = 5
  elif len(x) >= 70 and len(x) < 150:
      j = 10

  if len(x) < 150:
      while i <= len(x):
          tickx.append(i)
          i += j
  
      if x[-1] not in tickx:
          if (x[-1] - tickx[-1]) < 4:
              tickx[-1] = x[-1]
          else:
              tickx.append(x[-1])

      axes.set_xticks(tickx)

  axes.set_yticklabels(labely)
  

  X_Y_Spline = make_interp_spline(x, y)

  # Returns evenly spaced numbers
  # over a specified interval.
  X_ = np.linspace(x[0], x[-1], 100)
  Y_ = X_Y_Spline(X_)

  # Plotting the Graph
  plt.plot(X_, Y_)
  plt.xlabel('Games played')
  plt.ylabel('MMR')
  plt.title(username + '\'s MMR over time')

  plt.savefig('/home/ubuntu/discord_bot/testgraph.png', bbox_inches="tight")

  file1.close()
  plt.clf()

  return True


make_graph('fakinator')