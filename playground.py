import matplotlib.pyplot as plt
from quadClass import Quad
from adjustText import adjust_text

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

xnorm = [(i*10)/len(x) for i in x]
ynorm = [(i*10)/len(y) for i in y]

xi = 0.136*(10/2)
yi = 0.035*(10/2)

sq = Quad(xnorm[0], ynorm[0] + 1, xi, yi)

tr = sq.get_botRight()
xnorm.append(tr[0])
ynorm.append(tr[1])

plt.scatter(x, y)

texts = []
texts.append(plt.text(s='13/07/22', x=6, y=6,
                            color="red",
                            bbox=dict(boxstyle="round, pad=0.1", fc="yellow")))

texts.append(plt.text(s='13/07/22', x=7, y=6,
                            color="red",
                            bbox=dict(boxstyle="round, pad=0.1", fc="yellow")))


adjust_text(texts, arrowprops=dict(arrowstyle='->'), force_points=10)

#, x=x, y=y, autoalign='y', only_move={'points':'y', 'text':'y'}, force_points=2, arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4}

plt.show()


