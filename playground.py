

week = []

with open('testweek.csv', 'r') as f:
    for line in f.readlines():
        day = line.split(',')
        Morning = int(day[0])
        Afternoon = int(day[1])
        Evening = int(day[2])
        Night = int(day[3][0])
        week.append([Morning, Afternoon, Evening, Night])

grid = "          Morning    Afternoon   Evening   Night\n"
weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for i in range(len(week)):
    grid += weekDays[i].ljust(9) + str(week[i][0]).rjust(5) + str(week[i][1]).rjust(13) + str(week[i][2]).rjust(10) + str(week[i][3]).rjust(9) + '\n'

print(grid)