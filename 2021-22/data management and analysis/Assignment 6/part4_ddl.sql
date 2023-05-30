drop table if exists descriptions;
create table descriptions (
	product_code text not null primary key,
	description text not null
);

drop table if exists terms;
create table terms (
	term_id serial not null primary key,
	term text not null
);

drop table if exists outcomes;
create table outcomes (
	outcome_id serial not null primary key,
	outcome text not null
);

drop table if exists reports;
create table reports (
	report_id varchar(255) not null primary key,
	created_date date not null,
	event_date date,
	patient_age integer,
	age_units varchar(10),
	sex varchar(2)
);

drop table if exists products;
create table products (
    product_id serial not null primary key,
    report_id varchar(255) not null references reports (report_id),
    product_type text not null,
    product text not null,
    product_code text not null references descriptions (product_code)
);

drop table if exists reports_terms;
create table reports_terms (
	report_id varchar(255) not null primary key references reports (report_id),
	term_id integer not null references terms (term_id)
);

drop table if exists reports_outcomes;
create table reports_outcomes (
	report_id varchar(255) not null primary key references reports (report_id),
	outcome_id integer not null references outcomes (outcome_id)
);
