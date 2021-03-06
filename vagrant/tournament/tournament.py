#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from zlib import crc32


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # connect to tournament database
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # delete every row in match table and commit
    c.execute("delete from match")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # delete every row in player table and commit
    c.execute("delete from player")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) as num from player")
    count = c.fetchall()[0][0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into player (name) values (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select id, name, wins, matches from standings")
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into match (winner, loser) values (%s, %s)",
              (winner, loser))
    conn.commit()
    conn.close()


def nextMatch():
    """Returns a tuple with next match players

    Returns:
      A touple containing (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    return swissPairings()[0]


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    # use a seed specific to current player list and round number
    c.execute("select setseed(%s)", (seed(),))

    # get players ordered by wins
    # players with same wins count are shuffled
    c.execute("select id, name from player_points "
              "order by matches, wins desc, random()")
    players = c.fetchall()
    conn.close()

    # split players into two groups to assign pairs
    first_group = players[0::2]
    second_group = players[1::2]

    # construct list of tuples pairings
    pairings = []
    for index in range(len(second_group)):
        pairings += [(first_group[index][0], first_group[index][1],
                     second_group[index][0], second_group[index][1])]

    return pairings


def getRoundNumber():
    conn = connect()
    c = conn.cursor()

    c.execute("select min(matches) from standings")
    roundNumber = c.fetchall()[0][0] + 1
    conn.close()

    return roundNumber


def seed():
    """Returns a float number that is the seed to be used at players pairing.
    This takes into account the current round for this tournament, so at every
    round players at each point group are shuffled differently.
    """
    conn = connect()
    c = conn.cursor()

    roundNumber = str(getRoundNumber())

    c.execute("select name from player order by id")
    names = c.fetchall()
    conn.close()

    allNames = ""
    for name in names:
        allNames += name[0]
    return float(str(crc32(roundNumber+allNames)).replace("-", "")[:6])/1000000
