-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop tables to test new versions of the schema
drop view if exists standings;
drop view if exists player_points;
drop table if exists match;
drop table if exists player;

-- Players table. Contains every registered player for this tournament
create table player (
	id				serial primary key,
	name			varchar(64)
);

-- Matches table. Contains results for every played match
create table match (
	id 				serial primary key,
	winner			integer references player(id),
	loser			integer references player(id)
);

-- This view is for internal use. We need it to be unordered so random numbers
-- assigned to each player remain the same during current round of games.
-- This way player pairings for the round keep the same if other games have
-- been played
create view player_points as 
	select wins_table.id, name, wins, (wins + loses) as matches from 
		(select player.id, name, count(winner) as wins from player 
			left join match on player.id=winner group by player.id)
			as wins_table
		join
		(select player.id, count(loser) as loses from player 
			left join match on player.id=loser group by player.id)
			as loses_table
		on wins_table.id=loses_table.id;

-- Standings view. Displays current positions for players in the tournament
-- It is constructed from the join of two different subqueries.
-- First subquery returns wins count for each player
-- Second subquery returns loses count for each player
-- The resulting table calculates column `matches` by adding wins + loses
create view standings as
	select id, name, wins, matches from player_points
	order by wins desc, matches desc, id;
