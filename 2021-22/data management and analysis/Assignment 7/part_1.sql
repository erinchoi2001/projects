-- 1. Write a query to show the report_id and the uppercase version of product for all rows that contain a 75 year old patient sorted by the report_id ascending.

select report_id, upper(product) as product
	from staging_caers_events
	where patient_age = 75 and age_units = 'year(s)'
	order by report_id asc;


-- 2. Use EXPLAIN ANALYZE to show how much time it takes to run your query

--                                                          QUERY PLAN                                                          
-- -----------------------------------------------------------------------------------------------------------------------------
--  Sort  (cost=2116.63..2117.52 rows=357 width=39) (actual time=12.683..12.733 rows=561 loops=1)
--    Sort Key: report_id
--    Sort Method: quicksort  Memory: 76kB
--    ->  Seq Scan on staging_caers_events  (cost=0.00..2101.49 rows=357 width=39) (actual time=0.082..12.117 rows=561 loops=1)
--          Filter: ((patient_age = 75) AND (age_units = 'year(s)'::text))
--          Rows Removed by Filter: 49879
--  Planning Time: 0.127 ms
--  Execution Time: 13.545 ms


-- 3a. Write SQL to add a single column index to make your query run faster and verify that it has been created by using \d your_table_name in psql

create index ix_patient_age on staging_caers_events(patient_age);
-- "ix_patient_age" btree (patient_age)


-- 3b. Write a 3rd query, a SELECT statement that involves the column you placed in the index on in the WHERE clause, that will cause the query planner to do a sequential scan rather than use the created index (that is, try to formulate a query that will make it not use the index)

-- explain analyze 
select report_id, upper(product) as product
	from staging_caers_events
	where patient_age <= 1000
	order by report_id asc;