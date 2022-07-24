import matplotlib.pyplot as plt
from quadClass import Quad

x = [1, 2, 3]
y = [1, 2, 3]

xnorm = [(i*10)/len(x) for i in x]
ynorm = [(i*10)/len(y) for i in y]

xi = 0.136*(10/2)
yi = 0.035*(10/2)

sq = Quad(xnorm[0], ynorm[0] + 1, xi, yi)

tr = sq.get_botRight()
xnorm.append(tr[0])
ynorm.append(tr[1])

plt.scatter(xnorm, ynorm)

#a = plt.annotate('13/07/22', xy=(x[0], y[0]), xytext=(x[0], y[0] + 1),arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4})
a = plt.annotate('13/07/22', xy=(xnorm[0], ynorm[0]), xytext=(xnorm[0], ynorm[0] + 1),arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4})

# Adding text on the plot.
bohn = plt.text(4, 6, 'test', style='italic', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 1})
bohnbox = bohn.get_bbox_patch().get_bbox()

print(bohnbox)

plt.show()


