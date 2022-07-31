import psycopg2
import os

def detuple(ls):
    '''
    This method strips away all the tuple wrappings of each element in the given list.
    '''
    for i in range(len(ls)):
        ls[i] = ls[i][0]
    return ls

def tupleToList(ls):
    '''
    This method turns a one-item list (the item being the tuple with information) 
    into a list of the items contained in the tuple.
    '''
    return list(ls[0])

def intersect(l1, l2):
    '''
    Find intersection between two lists.
    '''
    return [value for value in l1 if value in l2]


class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        Make sure you provide an implementation for your constructor! This is where you should initialize any of your instance variables and do any other necessary setup actions, like opening a database connection.
        '''
        self.connection = self.connect()
        pass

    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        DATABASE_URL = os.environ['DATABASE_URL']
        try:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            print("connection succeeded.")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    # The following functions are for executing commands

    def executeCommand(self, command):
        '''
        Execute given command, given no input, and return output from database.
        '''
        try:
            cursor = (self.connection).cursor()
            cursor.execute(command)
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
    
    def executeCommandName(self, command, name):
        '''
        Execute given command given name as input, and return output from database.
        '''
        try:
            cursor = (self.connection).cursor()
            cursor.execute(command, (name, ))
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
    
    def executeCommandGenre(self, command, genre):
        '''
        Execute given command given genre as input, and return output from database.
        '''
        try:
            cursor = (self.connection).cursor()
            cursor.execute(command, (genre, ))
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def executeCommandNat(self, command, nationality):
        '''
        Execute given command given nationality as input, and return output from database.
        '''
        try:
            cursor = (self.connection).cursor()
            cursor.execute(command, (nationality, ))
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def executeCommandYear(self, command, year):
        '''
        Execute given command given year as input, and return output from database.
        '''
        try:
            cursor = (self.connection).cursor()
            cursor.execute(command, (year, year))
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    # The following funtions are for getting all information for homepage form

    def getGenres(self):
        '''
        Returns a list of all unique genres spanned by all artists.
        '''
        query = "SELECT distinct genre FROM artist_genre ORDER BY genre ASC;"
        results = self.executeCommand(query)
        return detuple(results)
        

    def getNationalities(self):
        '''
        Returns a list of all unique nationalities spanned by all artists.
        '''
        query = "SELECT distinct nationality FROM artist_nationality ORDER BY nationality ASC;"
        results = self.executeCommand(query)
        return detuple(results)

    # The following functions are for user queries

    def getArtistsByName(self, inputName):
        '''
        Finds all the artists who have the name (case-insensitive).

        PARAMETERS:
            inputName - a string to search within all artist names for (not necessarily a valid artist name)
        RETURN:
            a list of for artists who have the name.
        '''
        query = "SELECT artist FROM artist_year_info WHERE LOWER(artist) LIKE LOWER(%s);"
        newInputName = "%%" + inputName + "%%"
        results = self.executeCommandName(query, newInputName)
        return detuple(results)

    def getArtistsByGenre(self, genre):
        '''
        Finds all the artists of the chosen genre.

        PARAMETERS:
            genre - a single chosen genre
        RETURN:
            list of artists who contributed to given genre
        '''
        query = "SELECT artist FROM artist_genre WHERE genre = %s ORDER BY artist;"
        results = self.executeCommandGenre(query, genre)
        return detuple(results)

    def getArtistsByNationality(self, nationality):
        '''
        Finds all the artists of the chosen nationality.

        PARAMETERS:
            nationality - a single chosen nationality
        RETURN:
            list of artists who had given nationality
        '''
        query = "SELECT artist FROM artist_nationality WHERE nationality = %s ORDER BY artist;"
        results = self.executeCommandNat(query, nationality)
        return detuple(results)

    def getArtistsByYear(self, year):
        '''
        Finds all the artists who were alive during a chosen year.

        PARAMETERS:
            year - a single chosen year
        RETURN:
            list of names of artists who were alive during a given year
        '''
        query = "SELECT artist FROM artist_year_info WHERE year_start <= %s AND year_end >= %s ORDER BY artist;"
        results = self.executeCommandYear(query, year)
        return detuple(results)

    def getArtistByMultiple(self, year, genre, nationality):
        '''
        Returns a list of name of artists that satisfy the given conditions.
        PARAMETERS:
            year - the year in which the artist was alive
            genre - the genre of the artist
            nationality - the nationality of the artist
        
        RETURN: 
            list of names of artists who satisfy the given conditions.
        '''
        if year == "" and genre == "null" and nationality == "null":
            query = "SELECT artist FROM artist_year_info;"
            results = self.executeCommand(query)
            return detuple(results)

        elif year == "" and genre == "null":
            return self.getArtistsByNationality(nationality)

        elif nationality == "null" and genre == "null":
            return self.getArtistsByYear(year)

        elif year == "" and nationality == "null":
            return self.getArtistsByGenre(genre)

        elif year == "":
            return intersect(self.getArtistsByNationality(nationality), self.getArtistsByGenre(genre))
        
        elif nationality == "null":
            return intersect(self.getArtistsByGenre(genre), self.getArtistsByYear(year))

        elif genre == "null":
            return intersect(self.getArtistsByNationality(nationality), self.getArtistsByYear(year))

        else:
            intersectionGenreNat = intersect(self.getArtistsByNationality(nationality), self.getArtistsByGenre(genre))
            return intersect(intersectionGenreNat, self.getArtistsByYear(year))

    # The following functions are for loading results page

    def getGenreOfArtist(self, name):
        '''
        Returns a list of genres that a given artist contributed to.

        PARAMETERS:
            name - a single chosen artist
        RETURN:
            list of genres that given artist contributed to
        '''
        query = "SELECT genre FROM artist_genre WHERE artist = %s;"
        results = self.executeCommandName(query, name)
        return detuple(results)

    def getNationalityOfArtist(self, name):
        '''
        Returns a list of nationalities that a given artist had.

        PARAMETERS:
            name - a single chosen artist
        RETURN:
            list of nationalities that given artist had
        '''
        query = "SELECT nationality FROM artist_nationality WHERE artist = %s;"
        results = self.executeCommandName(query, name)
        return detuple(results)

    def getInfoOfArtist(self, name):
        '''
        Returns years alive, bio, and wiki link (as link) for a given artist.

        PARAMETERS:
            name - a single chosen artist
        RETURN:
            list of info for given artist (indices 0-3 represent birth year, death year, bio, and wiki link)
        '''
        query = "SELECT * FROM artist_year_info WHERE artist = %s;"
        results = self.executeCommandName(query, name)
        return tupleToList(results)

    def combineArtistsInfo(self, artists):
        '''
        Compile a list of artist information given a list of names, 
        each dictionary contains all the information (nationality, genre, years, info)
        '''
        allArtists = []
        for a in artists:

            # name, years and info
            nameYearsBioWiki =  self.getInfoOfArtist(a)
            
            # genres
            genre = self.getGenreOfArtist(a)
            genreString = ', '.join(genre)

            #nationalities
            nat = self.getNationalityOfArtist(a)
            natString = ', '.join(nat)
            
            artistComboInfo = {'name' : nameYearsBioWiki[0],
                                'born' : nameYearsBioWiki[1],
                                'die' : nameYearsBioWiki[2],
                                'bio' : nameYearsBioWiki[3],
                                'wiki' : nameYearsBioWiki[4],
                                'nation' : natString,
                                'genres' : genreString}

            allArtists.append(artistComboInfo)

        return allArtists


if __name__ == '__main__':
    testObject = DataSource()

    print("results for getArtistsByGenre() : ", testObject.getArtistsByGenre('Impressionism'))
    print("results for getArtistsByNationality() : ", testObject.getArtistsByNationality('French'))
    print("results for getArtistsByYear() : ", testObject.getArtistsByYear(1500))
    print("results for getGenreOfArtist() : ", testObject.getGenreOfArtist('Paul Klee'))
    print("results for getNationalityOfArtist() : ", testObject.getNationalityOfArtist('Paul Klee'))

    print("results for getArtistsByGenre() : ", testObject.getArtistsByGenre('Imaginary Genre'))
    print("results for getArtistsByNationality() : ", testObject.getArtistsByNationality('Imaginary Nationality'))
    print("results for getArtistsByYear() : ", testObject.getArtistsByYear(3000))
    print("results for getGenreOfArtist() : ", testObject.getGenreOfArtist('Imaginary Artist'))
    print("results for getNationalityOfArtist() : ", testObject.getNationalityOfArtist('Imaginary Artist'))
    print('----------------------------------------------')
    
    print(testObject.getGenres())
    print(testObject.getNationalities())
    print(testObject.getArtistsByName('RENE'))
    print(testObject.getInfoOfArtist('Rene Magritte'))
    print('----------------------------------------------')
    
    print('All: ', testObject.getArtistByMultiple('', 'null', 'null'), '\n')
    print('Year: ', testObject.getArtistByMultiple('1904', 'null', 'null'), '\n')
    print('Nationality: ', testObject.getArtistByMultiple('', 'null', 'Spanish'), '\n')
    print('Genre: ', testObject.getArtistByMultiple('', 'Surrealism', 'null'), '\n')
    print('Genre * nationality: ', testObject.getArtistByMultiple('', 'Surrealism', 'Spanish'), '\n')
    print('Year * nationality: ', testObject.getArtistByMultiple('1904', 'null', 'Spanish'), '\n')
    print('Year * genre: ', testObject.getArtistByMultiple('1904', 'Surrealism', 'null'), '\n')
    print('Year * genre * nationality: ', testObject.getArtistByMultiple('1904', 'Surrealism', 'Spanish'), '\n')
    print('Year * genre * nationality: ', testObject.getArtistByMultiple('1550', 'High Renaissance', 'Italian'), '\n')
    
    pass