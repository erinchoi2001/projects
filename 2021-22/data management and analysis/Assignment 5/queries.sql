-- write your queries underneath each number:
 
-- 1. the total number of rows in the database
select count(*) from topsongs;

-- 2. show the first 15 rows, but only display 3 columns (your choice)
select title, artist, year from topsongs limit 15;

-- 3. do the same as above, but chose a column to sort on, and sort in descending order
select title, artist, year from topsongs order by artist desc limit 15;

-- 4. add a new column without a default value
alter table topsongs add column years_since_2010 integer;
\d topsongs

-- 5. set the value of that new column
update topsongs set years_since_2010 = year-2010;
select * from topsongs order by year desc limit 15;

-- 6. show only the unique (non duplicates) of a column of your choice
select distinct genre from topsongs;

-- 7. group rows together by a column value (your choice) and use an aggregate function to calculate something about that group 
select artist, count(artist) from topsongs group by artist;

-- 8. now, using the same grouping query or creating another one, find a way to filter the query results based on the values for the groups 
select artist, count(artist) from topsongs group by artist having count(artist) > 2;


-- My own queries:

-- 9. show the bpm values that occur at least 3 times, in descending order by count
select bpm, count(bpm) 
	from topsongs 
	group by bpm 
	having count(bpm) > 2 
	order by count(bpm) desc;

-- 10. show all the genres that occur at least 3 times, in alphabetical order
select genre, count(genre) 
	from topsongs 
	group by genre 
	having count(genre) > 2 
	order by genre;

-- 11. show songs (title) that have very fast tempos (at least 176 bpm) 
-- along with their tempos, with song titles in alphabetical order
select title, bpm from topsongs where bpm > 175 order by title;

-- 12. for all artists with at least 10 songs in the database, show the average bpm 
-- of their songs, in alphabetical order by artist name
select artist, count(artist), avg(bpm) 
	from topsongs
	group by artist
	having count(artist) > 9
	order by artist;

