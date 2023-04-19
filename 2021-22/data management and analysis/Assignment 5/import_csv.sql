-- write your COPY statement to import a csv here

\copy topsongs
FROM './Documents/erinchoi2001-homework05/topsongs2010s.csv'
csv HEADER;