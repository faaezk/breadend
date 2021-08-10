import matplotlib.pyplot as plt

def double_graph(user1, user2):
    x1 = [10,20,30]
    y1 = [20,40,10]

    plt.plot(x1, y1, label = "line 1")

    x2 = [10,20,30]
    y2 = [40,10,30]

    plt.plot(x2, y2, label = "line 2")
    
    plt.xlabel('Games played')
    plt.ylabel('MMR')

    plt.title(f'{user1}\'s and {user2}\'s MMR over time')

    plt.legend()

    plt.savefig('/Users/faaezkamal/GitKraken Stuff/discord_bot/tester.png', bbox_inches="tight")
    plt.clf()

double_graph("john", "flohn")