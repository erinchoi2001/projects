-- write your table creation sql here!

DROP TABLE IF EXISTS topsongs;
CREATE TABLE topsongs (
	id integer PRIMARY KEY,
	title varchar(200) NOT NULL,
	artist varchar(100) NOT NULL,
	genre varchar(100) NOT NULL,
	year integer NOT NULL,
	bpm integer NOT NULL
);
