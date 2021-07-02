import os

def listoCsv(jg):
    output = ""
    for elem in jg:
        output += str(elem) + ","
    
    return output[:-1] + '\n'

def day_time(day, time):

    d = None
    t = None

    if day == "monday":
        d = 0
    elif day == "tuesday":
        d = 1
    elif day == "wednesday":
        d = 2
    elif day == "thursday":
        d = 3
    elif day == "friday":
        d = 4
    elif day == "saturday":
        d = 5
    elif day == "sunday":
        d = 6

    if time == 'all':
        t = 'All'
    elif time == 'morning':
        t = 0
    elif time == 'afternoon':
        t = 1
    elif time == 'evening':
        t = 2
    elif time == 'night':
        t = 3

    return d, t

class Week():
    def __init__(self, filePath):
        self.filePath = filePath
        self.days = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def save(self):
        with open(self.filePath, "w+") as f:
            f.writelines([listoCsv(x) for x in self.days])

    def load(self):
        if os.path.isfile(self.filePath) == False:
            f = open(self.filePath, 'x')
            f.close()
        else:
            self.days = []
            with open(self.filePath, 'r') as f:
                for line in f.readlines():
                    day = line.split(',')
                    Morning = int(day[0])
                    Afternoon = int(day[1])
                    Evening = int(day[2])
                    Night = int(day[3][0])
                    self.days.append([Morning, Afternoon, Evening, Night])

    def getWeek(self):
        return self.days
    
    def clearWeek(self):
        self.days = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    
    def isEmpty(self):
        if self.days == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
            return True
        
        return False
    
    def freetime(self, inpot):

        inpot = inpot.split(', ')

        for elem in inpot:
            j = elem.split(' ')

            d, t = day_time(j[0], j[1])

            if t == 'All':
                self.days[d] = [x + 1 for x in self.days[d]]
            else:
                self.days[d][t] += 1

    def busy(self, inpot):

        inpot = inpot.split(', ')

        for elem in inpot:
            j = elem.split(' ')

            d, t = day_time(j[0], j[1])

            if t == 'All':
                self.days[d] = [x - 1 for x in self.days[d]]
            else:
                self.days[d][t] -= 1

    def bestTimes(self):
        top = []
        max = 1
        for i in range(len(self.days)):
            for j in range(len(self.days[i])):
                jg = int(self.days[i][j])
                if jg >= max:
                    max = jg
                    top.append([i,j])
        
        for time in top:
            if time[0] == 0:
                time[0] = 'Monday'
            elif time[0] == 1:
                time[0] = 'Tuesday'
            elif time[0] == 2:
                time[0] = 'Wednesday'
            elif time[0] == 3:
                time[0] = 'Thursday'
            elif time[0] == 4:
                time[0] = 'Friday'
            elif time[0] == 5:
                time[0] = 'Saturday'
            elif time[0] == 6:
                time[0] = 'Sunday'

            if time[1] == 0:
                time[1] = 'Morning'
            elif time[1] == 1:
                time[1] = 'Afternoon'
            elif time[1] == 2:
                time[1] = 'Evening'
            elif time[1] == 3:
                time[1] = 'Night'

        if top == []:
            return "No entries found"
        
        final = "Best Times:\n"
        
        for timeSlot in top:
            final += timeSlot[0] + " " + timeSlot[1] + '\n'

        return final


def freerTime(msg, week):
    week = Week(f'{week}.csv')
    week.load()
    week.freetime(msg)
    week.save()

def busyTime(msg, week):
    week = Week(f'{week}.csv')
    week.load()
    week.busy(msg)
    week.save()

def bestTimes(week):
    
    self = Week('{}.csv'.format(week))
    self.load()
    top = []
    max = 1
    for i in range(len(self.days)):
        for j in range(len(self.days[i])):
            jg = int(self.days[i][j])
            if jg >= max:
                max = jg
                top.append([i,j])
    
    for time in top:
        if time[0] == 0:
            time[0] = 'Monday'
        elif time[0] == 1:
            time[0] = 'Tuesday'
        elif time[0] == 2:
            time[0] = 'Wednesday'
        elif time[0] == 3:
            time[0] = 'Thursday'
        elif time[0] == 4:
            time[0] = 'Friday'
        elif time[0] == 5:
            time[0] = 'Saturday'
        elif time[0] == 6:
            time[0] = 'Sunday'

        if time[1] == 0:
            time[1] = 'Morning'
        elif time[1] == 1:
            time[1] = 'Afternoon'
        elif time[1] == 2:
            time[1] = 'Evening'
        elif time[1] == 3:
            time[1] = 'Night'

    if top == []:
        return "No entries found"
    
    final = "Best Times:\n"
    
    for timeSlot in top:
        final += timeSlot[0] + " " + timeSlot[1] + '\n'

    return final

if __name__ == '__main__':
    week = Week("testweek.csv")
    week.load()
    week.freetime("tuesday all, monday afternoon, thursday afternoon, sunday morning, friday night")
    week.save()
    week.busy("tuesday all, monday afternoon")
    #print(week.bestTimes())
    
    x = "$free week1 tuesday all, monday afternoon, thursday afternoon, sunday morning, friday night"

    x = x[6:]
    jg = x[0:5]
    week = Week(f'{jg}.csv')
    week.load()
    week.freetime(x[6:])
    week.save()

