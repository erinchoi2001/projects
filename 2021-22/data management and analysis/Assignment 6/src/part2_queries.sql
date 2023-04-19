-- 1. Show the possible values of the year column in the country_stats table sorted by most recent year first.

select distinct year from country_stats order by year desc;

-- 2. Show the names of the first 5 countries in the database when sorted in alphabetical order by name.

select name from countries order by name limit 5;

-- 3. Adjust the previous query to show both the country name and the gdp from 2018, but this time show the top 5 countries by gdp.

select name, gdp 
	from countries
	inner join country_stats on countries.country_id = country_stats.country_id
	where year = 2018
	order by gdp desc limit 5;

-- 4. How many countries are associated with each region id?

select region_id, count(region_id) as country_count
	from countries
	group by region_id
	order by country_count desc;

-- 5. What is the average area of countries in each region id?

select region_id, round(avg(area)) as avg_area
	from countries
	group by region_id
	order by avg_area asc;

-- 6. Use the same query as above, but only show the groups with an average country area less than 1000

select region_id, round(avg(area)) as avg_area
	from countries
	group by region_id
	having round(avg(area)) < 1000
	order by avg_area asc;

-- 7. Create a report displaying the name and population of every continent in the database from the year 2018 in millions.

select continents.name, round(((sum(population)::numeric)/1000000)::numeric, 2) as tot_pop
	from continents
	inner join regions on continents.continent_id = regions.continent_id
	inner join countries on regions.region_id = countries.region_id
	inner join country_stats on countries.country_id = country_stats.country_id
	where year = 2018
	group by continents.name
	order by tot_pop desc;

-- 8. List the names of all of the countries that do not have a language.

select name
	from countries
	left join country_languages 
	on countries.country_id = country_languages.country_id
	where language_id is null;

-- 9. Show the country name and number of associated languages of the top 10 countries with most languages

select name, count(language_id) as lang_count
	from countries
	inner join country_languages
		on countries.country_id = country_languages.country_id
	group by name
	order by lang_count desc, name asc limit 10;

-- 10. Repeat your previous query, but display a comma separated list of spoken languages rather than a count (use the aggregate function for strings, string_agg.

select name, string_agg(language, ',')
	from countries
	inner join country_languages
		on countries.country_id = country_languages.country_id
	inner join languages
		on country_languages.language_id = languages.language_id
	group by name
	order by count(country_languages.language_id) desc, name asc limit 10;

-- 11. What's the average number of languages in every country in a region in the dataset? Show both the region's name and the average. Make sure to include countries that don't have a language in your calculations. (Hint: using your previous queries and additional subqueries may be useful)

with lang_count_table as (
	select name, count(language_id) as lang_count
	from countries
	left join country_languages
		on countries.country_id = country_languages.country_id
	group by name
)
select regions.name, round((avg(lang_count))::numeric, 1) as avg_lang_count_per_country
	from regions
	left join countries
		on regions.region_id = countries.region_id
	left join lang_count_table
		on countries.name = lang_count_table.name
	group by regions.name
	order by avg_lang_count_per_country desc;

-- 12. Show the country name and its "national day" for the country with the most recent national day and the country with the oldest national day. Do this with a single query. (Hint: both subqueries and UNION may be helpful here).

select name, national_day
	from countries
	where national_day = (
		select min(national_day) from countries)
union
select name, national_day
	from countries
	where national_day = (
		select max(national_day) from countries);
