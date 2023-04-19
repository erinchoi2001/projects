-- 1. This query tries to determine if report_id is unique.

select report_id, count(*) as c 
	from staging_caers_events 
	group by report_id 
	order by c desc limit 10; 

--     report_id    | c  
-- -----------------+----
--  179852          | 44
--  174049          | 39
--  210074          | 35
--  190041          | 35
--  190166          | 30
--  198546          | 28
--  2017-CFS-002608 | 27
--  192894          | 27
--  194925          | 25
--  2017-CFS-000086 | 25


-- 2. This query tries to determine if report_id and product can make up a composite primary key.

select report_id, product, count(*) as c 
	from staging_caers_events 
	group by report_id, product 
	order by c desc limit 10;

--  report_id |   product   | c 
-- -----------+-------------+---
--  200371    | EXEMPTION 4 | 3
--  191731    | EXEMPTION 4 | 3
--  216086    | EXEMPTION 4 | 3
--  178211    | EXEMPTION 4 | 3
--  194882    | EXEMPTION 4 | 3
--  213904    | EXEMPTION 4 | 3
--  190797    | EXEMPTION 4 | 2
--  180058    | EXEMPTION 4 | 2
--  194811    | EXEMPTION 4 | 2
--  184317    | EXEMPTION 4 | 2


-- 3. This query tries to determine if report_id, product, product_type, and product_code can provide a candidate key.

select report_id, product, product_type, product_code, count(*) as c
	from staging_caers_events
	group by report_id,	product, product_type, product_code
	order by c desc limit 10;

--  report_id |                                                            product                                                            | product_type | product_code | c 
-- -----------+-------------------------------------------------------------------------------------------------------------------------------+--------------+--------------+---
--  183220    | ONE A DAY WOMENS VITACRAVES GUMMIES MULTIVITAMINS + MINERALS                                                                  | SUSPECT      | 54           | 1
--  182667    | EXEMPTION 4                                                                                                                   | SUSPECT      | 53           | 1
--  189122    | PRESERVISION AREDS PO                                                                                                         | CONCOMITANT  | 54           | 1
--  192097    | ONE A DAY WOMEN'S 50+ HEALTHY ADVANTAGE (MULTIVITAMINS + MINERALS) FILM-COATED TABLET                                         | SUSPECT      | 54           | 1
--  181333    | MET RX PROTEIN AND OATS COCOA POWDER (DIETARY SUPPLEMENT) POWDER                                                              | SUSPECT      | 54           | 1
--  184301    | EXEMPTION 4                                                                                                                   | SUSPECT      | 53           | 1
--  190326    | GLUTEN FREE CHEERIOS                                                                                                          | SUSPECT      | 5            | 1
--  173922    | LIVER CLEANSER                                                                                                                | SUSPECT      | 54           | 1
--  189453    | CITRACAL CALCIUM+ D SLOW RELEASE 1200 (CALCIUM CARBONATE, CALCIUM CITRATE, VITAMIN D, MAGNESIUM HYDROXIDE) FILM-COATED TABLET | SUSPECT      | 54           | 1
--  185571    | VITAMIN C                                                                                                                     | CONCOMITANT  | 54           | 1


-- 4. This query tries to determine if description is functionally dependent on report_id.

select report_id, description
	from staging_caers_events 
	where report_id = '210074' limit 10;

--  report_id |                  description                  
-- -----------+-----------------------------------------------
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Dietary Conventional Foods/Meal Replacements
--  210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
--  210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
--  210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
--  210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)


-- 5. This query tries to determine there is a partial key dependency of description on product code.

with code_desc as (
	select distinct product_code, description
	from staging_caers_events
	order by product_code desc nulls last
	)
select product_code, count(*) as c
	from code_desc
	group by product_code
	order by c desc limit 10;

--  product_code | c 
-- --------------+---
--  9            | 2
--  20           | 2
--  5            | 2
--  16           | 2
--  32           | 1
--  37           | 1
--  34           | 1
--  40O          | 1
--  2            | 1
--  4            | 1


-- 6. This query continues the previous query's goal by trying to determine if the descriptions for the product codes with counts of 2 above are actually the same.

select distinct product_code, description
	from staging_caers_events
	where product_code = '9'
	or product_code = '20'
	or product_code = '5'
	or product_code = '16'
	order by product_code desc;

--  product_code |         description          
-- --------------+------------------------------
--  9            |  Milk/Butter/Dried Milk Prod
--  9            | Milk/Butter/Dried Milk Prod
--  5            |  Cereal Prep/Breakfast Food
--  5            | Cereal Prep/Breakfast Food
--  20           |  Fruit/Fruit Prod
--  20           | Fruit/Fruit Prod
--  16           |  Fishery/Seafood Prod
--  16           | Fishery/Seafood Prod

-- 7. This query tries to determine if created_date is functionally dependent on report_id.

with temp as (
	select distinct report_id, created_date
	from staging_caers_events
	order by report_id desc nulls last
	)
select report_id, count(*) as c
	from temp
	group by report_id
	order by c desc limit 10;

--  report_id | c 
-- -----------+---
--  209126    | 1
--  183778    | 1
--  194867    | 1
--  209563    | 1
--  217147    | 1
--  181790    | 1
--  192754    | 1
--  208317    | 1
--  182359    | 1
--  203819    | 1
