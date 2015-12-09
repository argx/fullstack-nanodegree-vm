# P2: Tournament Results
## Introduction

This project allows to manage a tournament, using the Swiss pairings system.

Tournament data is stored in a database. Database schema and a set of python functions are provided to manage this data.

Tournament management can be performed through several functions defined at `tournament.py` script.

These are some of the available functions:

- countPlayers(): Returns the number of players that are already registered in the database.
- registerPlayer(name): Registers a new player in the tournament.
- playerStandings(): Returns a list of the players, sorted by the number of wins.
- reportMatch(winner, loser): Stores the result of a match between two players.
- swissPairings(): Returns pairings for the next round of matches.

Tournament can be reset, so we can manage a new tournament.

- deleteMatches(): Deletes all stored matches
- deletePlayers(): Deletes all registered players

Always delete matches before deleting players.

## Requirements

- Access to a PostgreSQL server

## Setup

Open a shell and cd to tournament folder where `tournament.sql` and `tournament.py` are located. 

```
$ cd tournament
```

### Create database 

and then connect to it
```
$ psql -c "create database tournament;"
$ psql tournament
```
### Import schema
```
tournament=> \i tournament.sql;
```
This will create two tables: `player` and `match`
And a view: `standings`

This command will drop previously created tables and view with these names.

go back to shell prompt
```
tournament=> \q
```

## Usage

Now that everything is set, we can use the library as needed.

A script named `my_tournament.py` has been included as an example.

You can try it out by running it in shell:
```
$ ./my_tournament.py
```