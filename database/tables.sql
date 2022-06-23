DROP TABLE IF EXISTS artist_year_info;
CREATE TABLE artist_year_info (
  artist text,
  year_start int,
  year_end int,
  bio text,
  link text
);

/* will have same artist in multiple rows if multiple genres */
DROP TABLE IF EXISTS artist_genre;
CREATE TABLE artist_genre (
  artist text,
  genre text
);

/* will have same artist in multiple rows if multiple nationalities */
DROP TABLE IF EXISTS artist_nationality;
CREATE TABLE artist_nationality (
  artist text,
  nationality text
);