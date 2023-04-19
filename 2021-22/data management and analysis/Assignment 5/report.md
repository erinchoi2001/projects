# Overview

The following documentation is about top10s.csv - topsongs2010s.csv is the data for my table in postgres, which is a transformed version of the original dataset that uses some of the columns from the original.

1. Name / Title: Top Spotify songs from 2010-2019 - BY YEAR
2. Link to Data: https://www.kaggle.com/leonardopena/top-spotify-songs-from-20102019-by-year
3. Source / Origin: 
	* Author or Creator: Leonardo Henrique
	* Publication Date: 12/26/19
	* Publisher: Leonardo Henrique on Kaggle
	* Version of Data Accessed: 1
4. License: None specified ("Other": data were extracted from http://organizeyourmusic.playlistmachinery.com/)

Format: .csv
Size: 54 kB (transformed data size is 35 kB)
Number of Records: 603

- Field/Column 1: # (song ID number, int)
- Field/Column 2: title (title of song, str)
- Field/Column 3: artist (song artist, str)
- Field/Column 4: top genre (genre of the song, str)
- Field/Column 5: year (year of song's release, int)
- Field/Column 6: bpm (tempo in beats per minute, int)
- Field/Column 7: nrgy (measure of how energetic the song is, int)
- Field/Column 8: dnce (danceability of song, int)
- Field/Column 9: dB (loudness in decibels, int)
- Field/Column 10: live (likeliness that song is a live recording, int)
- Field/Column 11: val (valence/positivity of song, int)
- Field/Column 12: dur (duration in seconds, int)
- Field/Column 13: acous (acousticness of song, int)
- Field/Column 14: spch (measure of how much spoken word is in the song, int)
- Field/Column 15: pop (how popular the song is, int)

Note: only columns 1-6 from the original data are included in the table.


# Table Design

Primary key (type): # (integer) - renamed as id in the table

Other column types:
- title: varchar(200)
- artist: varchar(100)
- top genre: varchar(100) - renamed as genre in the table
- year: integer
- bpm: integer

None of these columns should allow null values - all songs in the dataset have easily identifiable titles, artists, genres, years of release, and tempos in beats per minute. Thus there are no default values that these columns should be set to.

All of these columns (besides the primary key '#', which should only contain unique integer values for each entry) should allow for duplicates, since songs could (and do) have the same titles, artists, genres, years of release, and tempos.

Note about the primary key: if this column did not already exist in the data, the column would have been added as a serial type artificial primary key.


# Import

ERROR:  extra data after last expected column

CONTEXT:  COPY topsongs, line 2: "0,1,"Hey, Soul Sister",Train,neo mellow,2010,97"

This error occurred at first because the index of the pandas DataFrame was included in the new .csv file when I used .to_csv at first (e.g. index 0 for the first row of the file, which is shown in the context above). I had to re-save the csv with the index=False parameter, then the import worked just fine.


# Database Information

```
### 1. Show all databases in your postgres instance
                                List of databases
     Name     |    Owner     | Encoding | Collate | Ctype |   Access privileges   
--------------+--------------+----------+---------+-------+-----------------------
 erinchoi2001 | erinchoi2001 | UTF8     | C       | C     | 
 homework05   | erinchoi2001 | UTF8     | C       | C     | 
 postgres     | postgres     | UTF8     | C       | C     | 
 template0    | postgres     | UTF8     | C       | C     | =c/postgres          +
              |              |          |         |       | postgres=CTc/postgres
 template1    | postgres     | UTF8     | C       | C     | =c/postgres          +
              |              |          |         |       | postgres=CTc/postgres
 test         | postgres     | UTF8     | C       | C     | 
(6 rows)
```

```
### 2. Show all tables in your database
            List of relations
 Schema |   Name   | Type  |    Owner     
--------+----------+-------+--------------
 public | topsongs | table | erinchoi2001
(1 row)
```

```
### 3. Show information about the table you created and imported data into
                     Table "public.topsongs"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 id     | integer                |           | not null | 
 title  | character varying(200) |           | not null | 
 artist | character varying(100) |           | not null | 
 genre  | character varying(100) |           | not null | 
 year   | integer                |           | not null | 
 bpm    | integer                |           | not null | 
Indexes:
    "topsongs_pkey" PRIMARY KEY, btree (id)
```


# Query Results
```
### 1. the total number of rows in the database
 count 
-------
   603
(1 row)
```

```
### 2. show the first 15 rows, but only display 3 columns (your choice)
                   title                    |      artist       | year 
--------------------------------------------+-------------------+------
 Hey, Soul Sister                           | Train             | 2010
 Love The Way You Lie                       | Eminem            | 2010
 TiK ToK                                    | Kesha             | 2010
 Bad Romance                                | Lady Gaga         | 2010
 Just the Way You Are                       | Bruno Mars        | 2010
 Baby                                       | Justin Bieber     | 2010
 Dynamite                                   | Taio Cruz         | 2010
 Secrets                                    | OneRepublic       | 2010
 Empire State of Mind (Part II) Broken Down | Alicia Keys       | 2010
 Only Girl (In The World)                   | Rihanna           | 2010
 Club Can't Handle Me (feat. David Guetta)  | Flo Rida          | 2010
 Marry You                                  | Bruno Mars        | 2010
 Cooler Than Me - Single Mix                | Mike Posner       | 2010
 Telephone                                  | Lady Gaga         | 2010
 Like A G6                                  | Far East Movement | 2010
(15 rows)
```

```
### 3. do the same as above, but chose a column to sort on, and sort in descending order
                         title                          |    artist    | year 
--------------------------------------------------------+--------------+------
 #thatPOWER                                             | will.i.am    | 2013
 Some Nights                                            | fun.         | 2012
 We Are Young (feat. Janelle Mon�e)                     | fun.         | 2012
 Clarity                                                | Zedd         | 2013
 Stay The Night - Featuring Hayley Williams Of Paramore | Zedd         | 2014
 Stay                                                   | Zedd         | 2017
 True Colors                                            | Zedd         | 2016
 Get Low (with Liam Payne)                              | Zedd         | 2017
 I Want You To Know                                     | Zedd         | 2015
 Never Forget You                                       | Zara Larsson | 2015
 LIKE I WOULD                                           | ZAYN         | 2016
 I Don�t Wanna Live Forever (Fifty Shades Darker)       | ZAYN         | 2017
 Dusk Till Dawn - Radio Edit                            | ZAYN         | 2018
 PILLOWTALK                                             | ZAYN         | 2016
 Let Me                                                 | ZAYN         | 2018
(15 rows)
```

```
### 4. add a new column without a default value
                          Table "public.topsongs"
      Column      |          Type          | Collation | Nullable | Default 
------------------+------------------------+-----------+----------+---------
 id               | integer                |           | not null | 
 title            | character varying(200) |           | not null | 
 artist           | character varying(100) |           | not null | 
 genre            | character varying(100) |           | not null | 
 year             | integer                |           | not null | 
 bpm              | integer                |           | not null | 
 years_since_2010 | integer                |           |          | 
Indexes:
    "topsongs_pkey" PRIMARY KEY, btree (id)
```

```
### 5. set the value of that new column
 id  |                        title                         |     artist     |    genre     | year | bpm | years_since_2010 
-----+------------------------------------------------------+----------------+--------------+------+-----+------------------
 579 | Trampoline (with ZAYN)                               | SHAED          | electropop   | 2019 | 127 |                9
 586 | Sucker                                               | Jonas Brothers | boy band     | 2019 | 138 |                9
 575 | Someone You Loved                                    | Lewis Capaldi  | pop          | 2019 | 110 |                9
 578 | South of the Border (feat. Camila Cabello & Cardi B) | Ed Sheeran     | pop          | 2019 |  98 |                9
 582 | Good as Hell (feat. Ariana Grande) - Remix           | Lizzo          | escape room  | 2019 |  96 |                9
 585 | Beautiful People (feat. Khalid)                      | Ed Sheeran     | pop          | 2019 |  93 |                9
 573 | Memories                                             | Maroon 5       | pop          | 2019 |  91 |                9
 574 | Lose You To Love Me                                  | Selena Gomez   | dance pop    | 2019 | 102 |                9
 576 | Se�orita                                             | Shawn Mendes   | canadian pop | 2019 | 117 |                9
 577 | How Do You Sleep?                                    | Sam Smith      | pop          | 2019 | 111 |                9
 580 | Happier                                              | Marshmello     | brostep      | 2019 | 100 |                9
 581 | Truth Hurts                                          | Lizzo          | escape room  | 2019 | 158 |                9
 583 | Higher Love                                          | Kygo           | edm          | 2019 | 104 |                9
 584 | Only Human                                           | Jonas Brothers | boy band     | 2019 |  94 |                9
 587 | Don't Call Me Up                                     | Mabel          | dance pop    | 2019 |  99 |                9
(15 rows)
```

```
### 6. show only the unique (non duplicates) of a column of your choice
           genre           
---------------------------
 electro house
 australian hip hop
 folk-pop
 downtempo
 latin
 hollywood
 electronic trap
 candy pop
 edm
 british soul
 moroccan pop
 boy band
 atl hip hop
 brostep
 french indie pop
 chicago rap
 australian pop
 canadian pop
 permanent wave
 irish singer-songwriter
 neo mellow
 big room
 tropical house
 colombian pop
 pop
 detroit hip hop
 australian dance
 dance pop
 alternative r&b
 art pop
 indie pop
 contemporary country
 electropop
 acoustic pop
 hip hop
 barbadian pop
 alaska indie
 celtic rock
 baroque pop
 metropopolis
 escape room
 canadian latin
 belgian edm
 house
 canadian hip hop
 hip pop
 electro
 complextro
 danish pop
 canadian contemporary r&b
(50 rows)
```

```
### 7. group rows together by a column value (your choice) and use an aggregate function to calculate something about that group
          artist          | count 
--------------------------+-------
 Shawn Mendes             |    11
 Rihanna                  |    15
 Niall Horan              |     2
 Janet Jackson            |     1
 Carly Rae Jepsen         |     5
 Chris Brown              |     3
 John Legend              |     2
 The Black Eyed Peas      |     5
 Lady Gaga                |    14
 Paloma Faith             |     1
 LMFAO                    |     2
 Sean Kingston            |     1
 Mariah Carey             |     2
 Flo Rida                 |     2
 The Weeknd               |     5
 Cardi B                  |     3
 Kygo                     |     4
 Florence + The Machine   |     3
 Bebe Rexha               |     2
 Years & Years            |     1
 MAGIC!                   |     1
 Britney Spears           |     9
 Jonas Blue               |     1
 Shakira                  |     3
 Jennifer Hudson          |     1
 Alessia Cara             |     4
 DJ Snake                 |     2
 Owl City                 |     1
 Nelly Furtado            |     1
 Snakehips                |     1
 Lukas Graham             |     1
 Ricky Martin             |     1
 5 Seconds of Summer      |     1
 A Great Big World        |     1
 Miley Cyrus              |     5
 Hozier                   |     1
 J Balvin                 |     1
 Marshmello               |     2
 Jessie J                 |     3
 The Script               |     1
 3OH!3                    |     1
 Lost Frequencies         |     2
 Gym Class Heroes         |     1
 Lilly Wood and The Prick |     1
 Pharrell Williams        |     2
 Emeli Sand�              |     3
 Zedd                     |     6
 Jennifer Lopez           |    10
 Tinie Tempah             |     2
 DNCE                     |     7
 Ne-Yo                    |     1
 Ellie Goulding           |     5
 Mike Posner              |     3
 Taio Cruz                |     2
 SHAED                    |     1
 P!nk                     |     6
 Kesha                    |     9
 Ciara                    |     1
 Taylor Swift             |     8
 Clean Bandit             |     2
 Iggy Azalea              |     1
 Lizzo                    |     2
 Passenger                |     2
 Lewis Capaldi            |     1
 Daft Punk                |     2
 Eminem                   |     2
 OneRepublic              |     9
 Pitbull                  |    11
 Hilary Duff              |     2
 Charli XCX               |     1
 One Direction            |     7
 Demi Lovato              |     8
 Rudimental               |     2
 Joey Montana             |     1
 Sara Bareilles           |     1
 Drake                    |     2
 David Guetta             |     9
 Coldplay                 |     4
 Ansel Elgort             |     1
 Robin Thicke             |     2
 N.E.R.D                  |     1
 Tove Lo                  |     2
 Jewel                    |     1
 Fergie                   |     3
 Troye Sivan              |     1
 Christina Aguilera       |     6
 Adam Lambert             |     2
 G-Eazy                   |     2
 Justin Bieber            |    16
 Hot Chelle Rae           |     1
 Enrique Iglesias         |     5
 Dan + Shay               |     1
 Hailee Steinfeld         |     3
 James Arthur             |     1
 Ariana Grande            |     9
 Meghan Trainor           |     6
 Labrinth                 |     1
 Sia                      |     6
 Icona Pop                |     1
 Sleeping At Last         |     1
 Lea Michele              |     1
 Maroon 5                 |    15
 Disclosure               |     1
 Train                    |     1
 Daddy Yankee             |     1
 Gwen Stefani             |     3
 Alicia Keys              |     6
 The Chainsmokers         |    11
 T.I.                     |     2
 Katy Perry               |    17
 Selena Gomez             |     8
 Charlie Puth             |     3
 Jess Glynne              |     1
 ZAYN                     |     5
 Selena Gomez & The Scene |     2
 Mabel                    |     1
 Sam Smith                |     3
 Kelly Clarkson           |     5
 Fifth Harmony            |     4
 Avril Lavigne            |     2
 R3HAB                    |     1
 Hayley Kiyoko            |     1
 Camila Cabello           |     3
 Jason Derulo             |     4
 Little Mix               |     5
 Lana Del Rey             |     4
 Madonna                  |     2
 Adele                    |    10
 fun.                     |     2
 Christina Perri          |     3
 Luis Fonsi               |     1
 Alesso                   |     1
 Wiz Khalifa              |     1
 Khalid                   |     1
 Robin Schulz             |     2
 Missy Elliott            |     2
 Nicki Minaj              |     6
 Galantis                 |     1
 Jonas Brothers           |     3
 Cashmere Cat             |     2
 B�RNS                    |     1
 Beyonc�                  |     8
 Usher                    |     2
 DJ Khaled                |     3
 Halsey                   |     1
 Neon Trees               |     2
 Zara Larsson             |     1
 Macklemore & Ryan Lewis  |     3
 Martin Garrix            |     2
 Mr. Probz                |     1
 Michael Jackson          |     1
 Harry Styles             |     1
 Sigala                   |     2
 Naughty Boy              |     2
 Far East Movement        |     1
 Calvin Harris            |    10
 RedOne                   |     1
 Liam Payne               |     3
 Rita Ora                 |     2
 Silk City                |     1
 Bastille                 |     1
 Avicii                   |     3
 Kanye West               |     1
 Mark Ronson              |     3
 Swedish House Mafia      |     1
 Major Lazer              |     2
 Alan Walker              |     1
 Austin Mahone            |     2
 Dua Lipa                 |     3
 Bruno Mars               |    13
 Justin Timberlake        |     9
 John Newman              |     1
 Olly Murs                |     1
 Kelly Rowland            |     1
 Lily Allen               |     1
 Nick Jonas               |     4
 Lorde                    |     1
 Martin Solveig           |     1
 CNCO                     |     1
 M�                       |     1
 The Wanted               |     3
 Ed Sheeran               |    11
 Birdy                    |     5
 will.i.am                |     1
(184 rows)
```

```
### 8. now, using the same grouping query or creating another one, find a way to filter the query results based on the values for the groups
         artist          | count 
-------------------------+-------
 Shawn Mendes            |    11
 Rihanna                 |    15
 Carly Rae Jepsen        |     5
 Chris Brown             |     3
 The Black Eyed Peas     |     5
 Lady Gaga               |    14
 The Weeknd              |     5
 Cardi B                 |     3
 Kygo                    |     4
 Florence + The Machine  |     3
 Britney Spears          |     9
 Shakira                 |     3
 Alessia Cara            |     4
 Miley Cyrus             |     5
 Jessie J                |     3
 Emeli Sand�             |     3
 Zedd                    |     6
 Jennifer Lopez          |    10
 DNCE                    |     7
 Ellie Goulding          |     5
 Mike Posner             |     3
 P!nk                    |     6
 Kesha                   |     9
 Taylor Swift            |     8
 OneRepublic             |     9
 Pitbull                 |    11
 One Direction           |     7
 Demi Lovato             |     8
 David Guetta            |     9
 Coldplay                |     4
 Fergie                  |     3
 Christina Aguilera      |     6
 Justin Bieber           |    16
 Enrique Iglesias        |     5
 Hailee Steinfeld        |     3
 Ariana Grande           |     9
 Meghan Trainor          |     6
 Sia                     |     6
 Maroon 5                |    15
 Gwen Stefani            |     3
 Alicia Keys             |     6
 The Chainsmokers        |    11
 Katy Perry              |    17
 Selena Gomez            |     8
 Charlie Puth            |     3
 ZAYN                    |     5
 Sam Smith               |     3
 Kelly Clarkson          |     5
 Fifth Harmony           |     4
 Camila Cabello          |     3
 Jason Derulo            |     4
 Little Mix              |     5
 Lana Del Rey            |     4
 Adele                   |    10
 Christina Perri         |     3
 Nicki Minaj             |     6
 Jonas Brothers          |     3
 Beyonc�                 |     8
 DJ Khaled               |     3
 Macklemore & Ryan Lewis |     3
 Calvin Harris           |    10
 Liam Payne              |     3
 Avicii                  |     3
 Mark Ronson             |     3
 Dua Lipa                |     3
 Bruno Mars              |    13
 Justin Timberlake       |     9
 Nick Jonas              |     4
 The Wanted              |     3
 Ed Sheeran              |    11
 Birdy                   |     5
(71 rows)
```

```
### 9. show the bpm values that occur at least 3 times, in descending order by count
 bpm | count 
-----+-------
 120 |    47
 100 |    33
 128 |    29
 130 |    27
 125 |    21
 126 |    20
 122 |    16
  95 |    14
 127 |    12
 124 |    12
 105 |    11
 110 |    11
 104 |    10
 102 |    10
  93 |    10
  92 |     9
 150 |     8
  90 |     8
  94 |     8
 140 |     8
 108 |     8
 118 |     8
 160 |     7
 121 |     7
 129 |     7
 123 |     7
 113 |     7
 103 |     7
 114 |     7
  86 |     7
 116 |     6
  96 |     6
  80 |     6
  97 |     6
 112 |     6
  98 |     6
  82 |     6
 136 |     6
  99 |     5
 148 |     5
  91 |     5
 144 |     5
 134 |     5
 107 |     5
 106 |     5
 138 |     5
  87 |     5
  77 |     4
 139 |     4
 111 |     4
 115 |     4
 186 |     4
 132 |     3
  83 |     3
 131 |     3
 117 |     3
 135 |     3
 142 |     3
 158 |     3
 109 |     3
 119 |     3
 190 |     3
 192 |     3
 146 |     3
  79 |     3
  84 |     3
 145 |     3
(67 rows)
```

```
### 10. show the genres that occur at least 3 times in alphabetical order
           genre           | count 
---------------------------+-------
 art pop                   |     8
 atl hip hop               |     5
 australian dance          |     6
 australian pop            |     5
 barbadian pop             |    15
 big room                  |    10
 boy band                  |    15
 british soul              |    11
 canadian contemporary r&b |     9
 canadian pop              |    34
 colombian pop             |     3
 complextro                |     6
 dance pop                 |   327
 edm                       |     5
 electropop                |    13
 hip hop                   |     4
 hip pop                   |     6
 latin                     |     4
 neo mellow                |     9
 permanent wave            |     4
 pop                       |    60
 tropical house            |     3
(22 rows)
```

```
### 11. show songs (title) that have very fast tempos (at least 176 bpm) along with their tempos, with song titles in alphabetical order
                       title                       | bpm 
---------------------------------------------------+-----
 Animals                                           | 190
 Brave                                             | 185
 Chained To The Rhythm                             | 190
 Despacito - Remix                                 | 178
 Dusk Till Dawn - Radio Edit                       | 180
 FourFiveSeconds                                   | 206
 Genie In a Bottle                                 | 176
 Hard                                              | 182
 How Far I'll Go - From "Moana"                    | 181
 How Ya Doin'? (feat. Missy Elliott)               | 201
 I'll Show You                                     | 192
 L.A.LOVE (la la)                                  | 202
 Love Me Like You Do - From "Fifty Shades Of Grey" | 190
 Partition                                         | 186
 Picky - Remix                                     | 186
 Roar                                              | 180
 Rock N Roll                                       | 184
 Shot Me Down (feat. Skylar Grey) - Radio Edit     | 192
 Starboy                                           | 186
 The Greatest                                      | 192
 We Are Young (feat. Janelle Mon�e)                | 184
 Whataya Want from Me                              | 186
(22 rows)
```

```
### 12. for all artists with at least 10 songs in the database, show the average bpm of their songs, in alphabetical order by artist name
      artist      | count |         avg          
------------------+-------+----------------------
 Adele            |    10 | 131.1000000000000000
 Bruno Mars       |    13 | 126.1538461538461538
 Calvin Harris    |    10 | 122.6000000000000000
 Ed Sheeran       |    11 | 101.2727272727272727
 Jennifer Lopez   |    10 | 122.0000000000000000
 Justin Bieber    |    16 | 111.6250000000000000
 Katy Perry       |    17 | 132.2352941176470588
 Lady Gaga        |    14 | 120.1428571428571429
 Maroon 5         |    15 | 118.4000000000000000
 Pitbull          |    11 | 125.3636363636363636
 Rihanna          |    15 | 125.3333333333333333
 Shawn Mendes     |    11 | 129.1818181818181818
 The Chainsmokers |    11 | 110.9090909090909091
(13 rows)
```
