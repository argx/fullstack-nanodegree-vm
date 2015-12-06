-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop table if exists match;
drop table if exists player;

create table player (
	id				serial primary key,
	name			varchar(64)
);

create table match (
	id 				serial primary key,
	winner			integer references player(id),
	loser			integer references player(id)
);

insert into player (name, lastname) values
	('Lionel Messi'),
	('Cristiano Ronaldo'),
	('Luis Suárez'),
	('Gareth Bale'),
	('Andrés Iniesta'),
	('Neymar Santos'),
	('Arturo Vidal'),
	('Arjen Robben'),
	('Zlatan Ibrahimović'),
	('Ángel di María'),
	('Manuel Neuer'),
	('Toni Kroos'),
	('Thiago Silva'),
	('Marco Reus'),
	('Sergio Busquets'),
	('James Rodríguez'),
	('Frank Ribéry'),
	('Sergio Agüero'),
	('Thomas Müller'),
	('Philipp Lahm');
