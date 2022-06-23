'''
Web application for CS 257 team I
CS 257, Spring 2021
'''

import flask
from flask import render_template, request
import json
import sys
sys.path.append('./backend/')
from datasource import DataSource


app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def homePage():
    '''
    Home page
    '''
    data = DataSource()
    gs = data.getGenres()
    ns = data.getNationalities()

    # render homepage with nations/genre options
    return render_template('index.html', genres=gs, nationalities=ns)

@app.route('/data')
def aboutData():
    '''
    About datapage
    '''
    return render_template("data.html") 


@app.route('/results', methods=['POST', 'GET'])
def results():
    '''
    Results page
    '''
    if request.method == 'POST':
        queries = request.form
        print(queries)

    data = DataSource()
    artists = []
    if 'a_name' in queries.keys(): # query is find by artist name
        artists = data.getArtistsByName(queries['a_name'])
    else: # query is filtering based on 3 criteria
        artists = data.getArtistByMultiple(queries['year'], queries['genre'], queries['nation'])
    
    # Get the combined information
    combinedInfo = data.combineArtistsInfo(artists)

    # Building queries summary/note to display on results page
    nonemptyQueries = []
    for item in queries.values():
        if item != 'null' and item != '':
            nonemptyQueries.append(item)
    queryNote = ", ".join(nonemptyQueries)
    if len(queryNote) == 0:
        queryNote = 'All'

    # render results with all information
    return render_template('results.html', entries=combinedInfo, query_note=queryNote)

'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

