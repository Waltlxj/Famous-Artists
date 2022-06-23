/* check tables */
-- SELECT * FROM artist_year_info;
-- SELECT * FROM artist_genre;
-- SELECT * FROM artist_nationality;

/* alphabetically list all artists who contributed to the genre "Impressionism" */
SELECT artist FROM artist_genre
WHERE genre = 'Impressionism'
ORDER BY artist;

/* alphabetically list all artists who had the nationality "French" */
SELECT artist FROM artist_nationality
WHERE nationality = 'French'
ORDER BY artist;

/* alphabetically list all artists who contributed to the genre "Impressionism" and had the nationality "French" */
SELECT artist FROM artist_genre
WHERE genre = 'Impressionism'
AND artist IN 
(SELECT artist FROM artist_nationality
WHERE nationality = 'French')
ORDER BY artist;

/* alphabetically list all artists alive during the year "1500" */
SELECT artist FROM artist_year_info
WHERE year_start <= 1500 AND year_end >= 1500
ORDER BY artist;

/* list all info (birth year, death year, bio, link, genres, nationalities) for artist "Paul Klee" */
SELECT year_start, year_end, bio, link FROM artist_year_info
WHERE artist = 'Paul Klee';

SELECT genre FROM artist_genre
WHERE artist = 'Paul Klee';

SELECT nationality FROM artist_nationality
WHERE artist = 'Paul Klee';
