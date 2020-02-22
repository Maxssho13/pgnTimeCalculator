#!/usr/bin/env python3
import math
import sys
import os

class Game:
    def __init__(self, player1="", player2="", winner=0, startTime=0, increment=0, totalWhite=0, totalTime=0, totalBlack=0):
        self.white = player1
        self.black = player2
        self.winner = winner
        self.startTime = startTime
        self.increment = increment
        self.totalWhite = totalWhite
        self.totalBlack = totalBlack
        self.totalTime = totalTime

def main():
    games = []
    # all games in specified folder
    dirs = os.listdir(sys.argv[1])
    dirs.remove(".DS_Store")

    for i in range(len(dirs)):
        games.append(Game())

        dirname = os.path.dirname(__file__)
        fn = os.path.join(dirname, sys.argv[1]+"/"+dirs[i])

        file = open(fn,"r")

        f1 = file.readlines()

        # grab players
        if "Maxssho13" in f1[4]:
            white = "Maxssho13"
            black = f1[5][8:len(f1[5])-3]
        else:
            white = f1[4][8:len(f1[4])-3]
            black = "Maxssho13"


        games[i].player1 = white
        games[i].player2 = black
        # winner: 1 = black win, 0 = white win
        games[i].winner = int(f1[6][9:len(f1[6])-5])

        splitTime = f1[10].split("+")
        games[i].startTime = int(splitTime[0][14:len(splitTime[0])])
        games[i].increment = int(splitTime[1][0:len(splitTime[1])-3])


        lastLineTimes = f1[len(f1)-1].split("%clk ")


        if len(lastLineTimes) > 2:
        # if both end times are on last line
            if f1[len(f1)-1][3] == ".":
                games[i].totalWhite = games[i].startTime - (int(lastLineTimes[2][0])*3600+int(lastLineTimes[2][2:4])*60+float(lastLineTimes[2][5:9]))
                games[i].totalBlack = games[i].startTime - (int(lastLineTimes[1][0])*3600+int(lastLineTimes[1][2:4])*60+float(lastLineTimes[1][5:9]))
            else:
                games[i].totalWhite = games[i].startTime - (int(lastLineTimes[1][0])*3600+int(lastLineTimes[1][2:4])*60+float(lastLineTimes[1][5:9]))
                games[i].totalBlack = games[i].startTime - (int(lastLineTimes[2][0])*3600+int(lastLineTimes[2][2:4])*60+float(lastLineTimes[2][5:9]))
        # 1 end time on last line. 1 on 2nd to last
        else:
            print(f1[len(f1)-2])




        games[i].totalTime = games[i].totalBlack + games[i].totalWhite
        games[i].totalTime += int(f1[len(f1)-1].split(".")[0]) * 2 * games[i].increment

        print(math.floor(games[i].totalTime/60), round(games[i].totalTime%60*10)/10)
        file.close()

main()
