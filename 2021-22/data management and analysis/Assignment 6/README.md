## Part 1: Create an ER Diagram by inspecting tables

- continents has a one-to-many relationship with regions because there is a foreign key in regions that references continent_id in continents.

- region_areas has a one-to-one relationship with regions because one value in the region_name column of region_areas corresponds to one value in the name column of regions. (This is shown as a one-to-many relationship in the diagram due to pgAdmin's restrictions.)

- regions has a one-to-many relationship with countries because there is a foreign key in countries that references region_id in regions.

- countries has a one-to-many relationship with country_stats because there is a foreign key in country_stats that references country_id in countries.

- countries has a one-to-many relationship with country_languages because there is a foreign key in country_languages that references country_id in countries.

- languages has a one-to-many relationship with country_languages because there is a foreign key in country_languages that references language_id in languages.


## Part 3: Examine a data set and create a normalized data model to store the data

```
### 1. This query tries to determine if report_id is unique.

    report_id    | c  
-----------------+----
 179852          | 44
 174049          | 39
 210074          | 35
 190041          | 35
 190166          | 30
 198546          | 28
 2017-CFS-002608 | 27
 192894          | 27
 194925          | 25
 2017-CFS-000086 | 25

report_id is not unique, so it alone cannot constitute a primary key.
```

```
### 2. This query tries to determine if report_id and product can make up a composite primary key.

 report_id |   product   | c 
-----------+-------------+---
 200371    | EXEMPTION 4 | 3
 191731    | EXEMPTION 4 | 3
 216086    | EXEMPTION 4 | 3
 178211    | EXEMPTION 4 | 3
 194882    | EXEMPTION 4 | 3
 213904    | EXEMPTION 4 | 3
 190797    | EXEMPTION 4 | 2
 180058    | EXEMPTION 4 | 2
 194811    | EXEMPTION 4 | 2
 184317    | EXEMPTION 4 | 2

 report_id and product together do not result in unique rows, so they cannot make up a composite key by themselves.
 ```

 ```
 ### 3. This query tries to determine if report_id, product, product_type, and product_code can provide a candidate key.

  report_id |                                                            product                                                            | product_type | product_code | c 
-----------+-------------------------------------------------------------------------------------------------------------------------------+--------------+--------------+---
 183220    | ONE A DAY WOMENS VITACRAVES GUMMIES MULTIVITAMINS + MINERALS                                                                  | SUSPECT      | 54           | 1
 182667    | EXEMPTION 4                                                                                                                   | SUSPECT      | 53           | 1
 189122    | PRESERVISION AREDS PO                                                                                                         | CONCOMITANT  | 54           | 1
 192097    | ONE A DAY WOMEN'S 50+ HEALTHY ADVANTAGE (MULTIVITAMINS + MINERALS) FILM-COATED TABLET                                         | SUSPECT      | 54           | 1
 181333    | MET RX PROTEIN AND OATS COCOA POWDER (DIETARY SUPPLEMENT) POWDER                                                              | SUSPECT      | 54           | 1
 184301    | EXEMPTION 4                                                                                                                   | SUSPECT      | 53           | 1
 190326    | GLUTEN FREE CHEERIOS                                                                                                          | SUSPECT      | 5            | 1
 173922    | LIVER CLEANSER                                                                                                                | SUSPECT      | 54           | 1
 189453    | CITRACAL CALCIUM+ D SLOW RELEASE 1200 (CALCIUM CARBONATE, CALCIUM CITRATE, VITAMIN D, MAGNESIUM HYDROXIDE) FILM-COATED TABLET | SUSPECT      | 54           | 1
 185571    | VITAMIN C                                                                                                                     | CONCOMITANT  | 54           | 1

These columns may provide a candidate key as grouping by all of them together produces unique values (counts of 1).
```

```
### 4. This query tries to determine if description is functionally dependent on report_id.

 report_id |                  description                  
-----------+-----------------------------------------------
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Dietary Conventional Foods/Meal Replacements
 210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
 210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
 210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)
 210074    |  Vit/Min/Prot/Unconv Diet(Human/Animal)

 The most frequently occurring report_id values (found in query 1) were entered in the where clause to check if there were different descriptions for any of them. Using report_id 210074 in this query showed there are at least 2 different descriptions for this report_id, meaning description is not functionally dependent on report_id.
 ```

 ```
 ### 5. This query tries to determine there is a partial key dependency of description on product code.

 product_code | c 
--------------+---
 9            | 2
 20           | 2
 5            | 2
 16           | 2
 32           | 1
 37           | 1
 34           | 1
 40O          | 1
 2            | 1
 4            | 1

 Just from these results I cannot tell if there is a partial key dependency - I must examine the unique descriptions of the product codes with (description) counts of 2.
 ```

 ```
 ### 6. This query continues the previous query's goal by trying to determine if the descriptions for the product codes with counts of 2 above are actually the same.

 product_code |         description          
--------------+------------------------------
 9            |  Milk/Butter/Dried Milk Prod
 9            | Milk/Butter/Dried Milk Prod
 5            |  Cereal Prep/Breakfast Food
 5            | Cereal Prep/Breakfast Food
 20           |  Fruit/Fruit Prod
 20           | Fruit/Fruit Prod
 16           |  Fishery/Seafood Prod
 16           | Fishery/Seafood Prod

Examining the pairs of descriptions for each product code, it is clear these descriptions are actually the same but with different spacing at the beginning; so there is a partial key dependency of description on product_code.
```

```
### 7. This query tries to determine if created_date is functionally dependent on report_id.

 report_id | c 
-----------+---
 209126    | 1
 183778    | 1
 194867    | 1
 209563    | 1
 217147    | 1
 181790    | 1
 192754    | 1
 208317    | 1
 182359    | 1
 203819    | 1

 Since the counts of all unique report_id and created_date pairs are 1, created_date does appear to be functionally dependent on report_id.
 ```


## Part 3: Examine a data set and create a normalized data model to store the data

![ERD for CAERS data in 3NF](/img/part3_03_caers_er_diagram.png)

* Normalization occurred based on examination of the candidate key identified in query 3 above (report_id, product, product_type, and product_code).

* Both created_date and event_date are functionally dependent on report_id, so a new table (reports) was created with report_id (as the primary key) and the date columns. patient_age, age_units, and sex were also included in this table since there are no partial-key dependencies with report_id. the products table contains a foreign key that refers to report_id in reports.

* description is functionally dependent on product_code, so a new table descriptions was created with these two columns. products contains a foreign key that refers to product_code in descriptions.

* terms and outcomes are non-atomic in the original table, so the values in these columns should be separated into separate rows. the new columns would be called "term" and "outcome" (singular), and assuming these columns are now atomic, they would each have a many-to-many relationship with report_id. each of them are put into new tables (terms, outcomes) with a serial-type id. and these tables are connected to report_id in the reports table by a many-to-many relationship to generate join tables containing report_id and term_id or outcome_id respectively.
