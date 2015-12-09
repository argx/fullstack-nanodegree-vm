#!/usr/bin/env python
#
# Tournament example

from tournament import *
from math import log,ceil

def showStandings():
    """Prints a formatted Player Standings table"""
    print "%-22s %-10s %s" % ("Player Name", "Wins", "Matches")

    for row in playerStandings():
        print "%-22s %-10s %s" % (row[1], row[2], row[3])


def showPairings():
    """Prints the matches pairings"""
    for row in swissPairings():
        print "%s vs %s" % (row[1], row[3])


def populateRegistry():
    """Prompts for players names to be included in the tournament"""
    print ("\nLet's register this tournament's players. "
           "Enter each player's name.\nWhen you're done, enter the word "
           "'ready' or just leave the field empty")
    newPlayer = raw_input("Register new Player: ")
    while(newPlayer not in ["ready", ""] ):
        registerPlayer(newPlayer)
        newPlayer = raw_input("Register new Player: ")


def playRound(roundNumber):
    """Displays standings at the begining of the round, the matches to be
    played, and then asks for results of match one by one."""
    print "Let's take a look at the standings: \n"

    showStandings()

    currentRound = getRoundNumber()

    print "\nThese are the matches for round %s\n" % currentRound

    showPairings()

    while(currentRound == roundNumber):
        report = True
        print ("\nNext match is:\n"
               "1.- %s\n"
               "2.- %s\n" % (nextMatch()[1], nextMatch()[3]))
        winner = raw_input("Enter the number of the winner player: ")
        if(winner=="1"):
            winnerId = nextMatch()[0]
            loserId = nextMatch()[2]
        elif(winner=="2"):
            winnerId = nextMatch()[2]
            loserId = nextMatch()[0]
        else:
            report = False

        if(report):
            reportMatch(winnerId, loserId)

        currentRound = getRoundNumber()

# init database
deleteMatches()
deletePlayers()

print "\nWelcome to the tournament\n"

# get the players in the tournament
populateRegistry()

# count players and calculate number of rounds
playerCount = countPlayers()
maxRounds = int(ceil(log(playerCount,2)))

print "\nThere are %s registered players\n" % playerCount
print "We will play %s rounds" % maxRounds

# play all rounds
for i in range(1,maxRounds+1):
    playRound(i)

print "Tournamet is over, and the champion is %s! \n" % playerStandings()[0][1]

showStandings()
