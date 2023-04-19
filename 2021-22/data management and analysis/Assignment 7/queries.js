// 1. show exactly two documents from the listings collection in any order

db.listings.find().limit(2)

/*
{ _id: ObjectId("61a7b54606b36db172f8b7fc"),
  id: '7801',
  listing_url: 'https://www.airbnb.com/rooms/7801',
  scrape_id: '20211102175544',
  last_scraped: '2021-11-03',
  name: 'Sweet and Spacious Brooklyn Loft',
  description: 'A true open-plan loft in a repurposed factory building with beautiful sunlight, a king bed and comfy double futon, fully stocked kitchen with dishwasher, washer and dryer, custom cedar sauna, bathroom with tub and shower, and lots of lounging spaces.<br /><br /><b>The space</b><br />The apartment is an open-plan 1500 sq. ft. loft (140 sq m) with 5 large windows providing bright sunlight all day, located in an old factory building with many of the original finishes including tin ceilings, wooden beams and columns, and white brick walls. Very few of these original factory loft buildings remain in the neighborhood, and this space is quite special.<br /><br />Located in the very center of Williamsburg: just two blocks from the Bedford L train and two blocks from McCarren park! Stellar restaurants, bars, nightlife, and shopping are all steps away. Manhattan is just a 5-10 minute ride on the L train.<br /><br />The loft has a fully stocked kitchen with fridge, oven, microwave, dishwasher, an',
  neighborhood_overview: 'We\'ve lived here for over 10 years and watched as the neighborhood has transformed into the vibrant creative scene for which it has become renowned. When you arrive, you\'ll find a printout of our personal neighborhood favorite shops, restaurants, bars and more.',
  picture_url: 'https://a0.muscache.com/pictures/207102/56d6fc69_original.jpg',
  host_id: '21207', 
*/


// 2. find the possible values (distinct) that appear in the field,host_name

db.listings.distinct('host_name')

/*
 [
  "'Cil",
  '(Ari) HENRY LEE',
  '(Email hidden by Airbnb)',
  '-TheQueensCornerLot',
  '0123',
  '2018Serenity',
  '235 Bainbridge',
  '420spa',
  '475',
*/


// 3. choose one of the host names above and show exactly one listing from that host

db.listings.find(
	{host_name: '0123'}, 
	{_id: 0, 
		host_name: 1, 
		name: 1, 
		listing_url: 1
	}).limit(1)

/*
{ listing_url: 'https://www.airbnb.com/rooms/30735480',
  name: 'Neve recording studio',
  host_name: '0123' }
*/


// 4. choose three of the host names, and show all of the listings hosted by any of the three hosts

db.listings.find(
	{host_name: {$in: ['0123', '420spa', '475']}}, 
	{_id: 0, 
		name: 1, 
		host_name: 1, 
		neighbourhood_cleansed: 1, 
		price: 1
	}).sort({host_name: 1})

/*
{ name: 'Neve recording studio',
  host_name: '0123',
  neighbourhood_cleansed: 'Lower East Side',
  price: '$600.00' }
{ name: 'ENJOY THE 420 ENVIRONMENT  WITH RELAXING PERKS',
  host_name: '420spa',
  neighbourhood_cleansed: 'Allerton',
  price: '$100.00' }
{ name: 'Private Historic Bungalow -Sleeps 2-Flex Check In',
  host_name: '475',
*/


// 5. what are the top 10 (by review scores) that have at least two bedrooms (not just beds) in the borough of Brooklyn?

db.listings.find(
	{bedrooms: {$gte: 2}, 
	neighbourhood_group_cleansed: 'Brooklyn'}, 
	{_id: 0, 
		name: 1, 
		neighbourhood_cleansed: 1, 
		bedrooms: 1, 
		price: 1
	}).sort({review_scores_rating: -1}).limit(10)

/*
{ name: 'Spacious Brooklyn Duplex, Patio + Garden',
  neighbourhood_cleansed: 'Sunset Park',
  bedrooms: '2',
  price: '$275.00' }
{ name: '2 BR Duplex @ Box House Hotel',
  neighbourhood_cleansed: 'Greenpoint',
  bedrooms: '2',
  price: '$599.00' }
{ name: 'Gorgeous Park Slope, BK triplex 4BD',
  neighbourhood_cleansed: 'Park Slope',
*/


// 6. show the number of listings per host

db.listings.aggregate([
	{$group: {
		_id: "$host_name",
		listingsCount: {$sum: 1}
	}}])

/*
{ _id: 'Shaila & Alex', listingsCount: 1 }
{ _id: 'Shmuel', listingsCount: 1 }
{ _id: 'Loli', listingsCount: 2 }
{ _id: 'Sadio', listingsCount: 1 }
{ _id: 'Luc', listingsCount: 3 }
{ _id: 'Danny And Alex', listingsCount: 1 }
{ _id: 'Sebastien Rafael', listingsCount: 1 }
{ _id: 'Kosta', listingsCount: 1 }
{ _id: 'Sade', listingsCount: 3 }
{ _id: 'Mallorie', listingsCount: 1 }
*/

// 7. show the number of listings per host sorted in order of listings descending, with the field name containing host displayed as host rather than _id 

db.listings.aggregate([
	{$group: {
		_id: "$host_name",
		listingsCount: {$sum: 1}
	}},
	{$project: {
		listingsCount: 1,
		_id: 0,
		host: '$_id',
	}}]).sort({listingsCount: -1})

/*
{ listingsCount: 400, host: 'June' }
{ listingsCount: 311, host: 'Michael' }
{ listingsCount: 304, host: 'Blueground' }
{ listingsCount: 251, host: 'Karen' }
{ listingsCount: 238, host: 'David' }
{ listingsCount: 222, host: 'Jeniffer' }
{ listingsCount: 210, host: 'Alex' }
{ listingsCount: 178, host: 'Daniel' }
{ listingsCount: 175, host: 'John' }
{ listingsCount: 174, host: 'Eugene' }
*/


// 8. show the bedroom to bed ratio (aliased as bedroomBedRatio) for all listings in the borough (neighbourhood_group_cleansed) Brooklyn

db.listings.aggregate([
	{$match: {
		beds: {$gte: 1},
		bedrooms: {$gte: 1},
		neighbourhood_group_cleansed: "Brooklyn"}},
	{$project:
		{_id: 0,
			name: 1,
			neighbourhood_cleansed: 1,
			bedrooms: 1,
			beds: 1, 
			bedroomBedRatio: {$divide: ["$bedrooms", "$beds"]}
	}}]).sort({neighbourhood_cleansed: 1})

/* 
{ name: 'Brand New small 1 Bedroom apt in Brooklyn',
  neighbourhood_cleansed: 'Bath Beach',
  bedrooms: 1,
  beds: 1,
  bedroomBedRatio: 1 }
{ name: 'Private Queen room&bathroom in NEW Luxury Building',
  neighbourhood_cleansed: 'Bath Beach',
  bedrooms: 1,
  beds: 1,
  bedroomBedRatio: 1 }
*/


// 9. using the previous query as a foundation, find the average bedroom to bed ratio for each borough (neighbourhood_group_cleansed) using an aggregation

db.listings.aggregate([
	{$match: {
		bedrooms: {$gte: 1},
		beds: {$gte: 1}}},
	{$group: {
		_id: "$neighbourhood_group_cleansed",
		avgBedRatio: {$avg: {$divide: ["$bedrooms", "$beds"]}}
	}}]).sort({avgBedRatio: -1})

/*
{ _id: 'Brooklyn', avgBedRatio: 0.925893863719455 }
{ _id: 'Manhattan', avgBedRatio: 0.9020413600110374 }
{ _id: 'Queens', avgBedRatio: 0.88898632498287 }
{ _id: 'Bronx', avgBedRatio: 0.8876594739329029 }
{ _id: 'Staten Island', avgBedRatio: 0.83395660461987 }
*/


// 10. in borough (again, use neighbourhood_group_cleansed), Manhattan, find the average review_scores_rating per neighbourhood_cleansed as well as the number of listings per neighbourhood_cleansed… only show the neighbourhoods that have more than 100 listings… sorted in descending order of rating

db.listings.aggregate([{
	$match: {
		neighbourhood_group_cleansed: "Manhattan"
	}}, {
	$group: {
		_id: "$neighbourhood_cleansed",
		avgRating: {$avg: {$toDouble: "$review_scores_rating"}},
		countListings: {$sum: 1}
	}}, {
	$match: {
		countListings: {$gt: 100}
	}}]).sort({avgRating: -1})

/*
{ _id: 'West Village',
  avgRating: 4.700544554455446,
  countListings: 520 }
{ _id: 'Nolita',
  avgRating: 4.694313725490196,
  countListings: 212 }
{ _id: 'Gramercy',
  avgRating: 4.6808771929824555,
  countListings: 227 }
{ _id: 'Chinatown',
*/

