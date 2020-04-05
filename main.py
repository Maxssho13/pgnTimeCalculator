#!/usr/bin/env python3
import sys
import os
import re
from itertools import chain
from datetime import datetime


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
    # all games in specified folder
    dirs = os.listdir(sys.argv[1])
    dirs.remove(".DS_Store")
    if "report.txt" in dirs:
        dirs.remove("report.txt")
    games = []

    # loop through each file
    for i in range(len(dirs)):

        games.append(Game())

        dirname = os.path.dirname(__file__)
        # grabs file index 'i'
        fPath = os.path.join(dirname, sys.argv[1]+"/"+dirs[i])  # <--[i]

        file = open(fPath, "r")

        wholeFile = file.read()

        # find result of game
        result = re.findall("Result .*", wholeFile)
        if len(result[0]) > 13:
            games[i].winner = 0.5
        else:
            # 1 = white, 0 = black, 0.5 = draw
            games[i].winner = result[0][8]

            # go back to top of file
            file.seek(0)
            fileLines = file.readlines()

            moveTimes = []
            with open(fPath) as input_data:
                # Skips text before the beginning of the interesting block:
                for line in input_data:
                    if line.strip() == '':  # Or whatever test is needed
                        break
            # Reads text until the end of the block:
                for line in input_data:  # This keeps reading the file
                    # print(line)
                    moveTimes.append(re.findall(
                        "[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9].?[0-9]?", line))
                # change 2d list to 1d
                moveTimes = list(chain.from_iterable(moveTimes))

            # grab players
            if "Maxssho13" in fileLines[4]:
                white = "Maxssho13"
                black = fileLines[5][8:len(fileLines[5])-3]
            else:
                white = fileLines[4][8:len(fileLines[4])-3]
                black = "Maxssho13"

            games[i].player1 = white
            games[i].player2 = black

            # moveTimes = re.findall(
            # "[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9].?[0-9]?", wholeFile)

            timeControl = re.findall("TimeControl .*", wholeFile)
            times = [string for string in re.findall(
                "[0-9]*", timeControl[0]) if string != ""]

            # find start time and increment
            games[i].startTime = int(times[0])
            games[i].increment = int(times[1])

            if len(moveTimes) % 2 == 1:
                # black played last move
                lastMoveWhiteSecond = (int(moveTimes[-1][0]) * 60 * 60) + (int(moveTimes[-1][2])*600) + (
                    int(moveTimes[-1][3])*60) + (int(moveTimes[-1][5])*10) + (int(moveTimes[-1][6]))
                lastMoveBlackSecond = (int(moveTimes[len(moveTimes)-2][0]) * 60 * 60) + (int(moveTimes[len(moveTimes)-2][2]) * 600) + (
                    int(moveTimes[len(moveTimes)-2][3])*60)+(int(moveTimes[len(moveTimes)-2][5])*10) + (int(moveTimes[len(moveTimes)-2][6]))
            if len(moveTimes) % 2 == 0:
                # white played last move
                lastMoveBlackSecond = (int(moveTimes[-1][0]) * 60 * 60) + (int(moveTimes[-1][2])*600) + (
                    int(moveTimes[-1][3])*60) + (int(moveTimes[-1][5])*10) + (int(moveTimes[-1][6]))
                lastMoveWhiteSecond = (int(moveTimes[len(moveTimes)-2][0]) * 60 * 60) + (int(moveTimes[len(moveTimes)-2][2]) * 600) + (
                    int(moveTimes[len(moveTimes)-2][3])*60)+(int(moveTimes[len(moveTimes)-2][5])*10) + (int(moveTimes[len(moveTimes)-2][6]))

            games[i].totalWhite = games[i].startTime - \
                lastMoveWhiteSecond + len(moveTimes)/2*games[i].increment
            games[i].totalBlack = games[i].startTime - \
                lastMoveBlackSecond + len(moveTimes)/2*games[i].increment

            games[i].totalTime = games[i].totalBlack + games[i].totalWhite

            file.close()

    generatePath = os.path.join(dirname, sys.argv[1])
    outputFile = open(generatePath+"/report.txt", "a")
    if len(dirs) == 1:
        outputFile.write("This week I played "+str(i+1)+" game. \n")
    else:
        outputFile.write("This week I played "+str(i+1)+" games. \n")

    for i in range(len(games)):
        outputFile.write("Game "+str(i+1)+": " +
                         str(round(games[i].totalTime/60, 1))+" minutes\n")

    outputFile.close()


main()
