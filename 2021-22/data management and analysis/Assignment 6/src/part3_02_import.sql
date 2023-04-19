copy staging_caers_event (
	report_id, created_date, event_date, product_type, 
	product, product_code, description, patient_age, 
	age_units, sex, terms, outcomes)
    from './Downloads/caers.csv'
    (format csv, header, encoding 'LATIN1');