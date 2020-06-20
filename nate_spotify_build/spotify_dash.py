from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from spotify_api import SpotifyAPI
import requests

# create an instance of the API
client_id = '1efa46aff77347859b690fa4329ee6a1'
client_secret = '42e1c54ccba84332be2ef25987466119'
spotify = SpotifyAPI(client_id=client_id, client_secret=client_secret)

# initialize the app
APP = Flask(__name__)

# configure a database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# get some information to store
# define a simple function to test
def song_info():
    song_title = 'Banana pancakes'
    artist = 'jack johnson'

    result = spotify.search(query = {'track': f"{song_title}", 'artist': f"{artist}"}, search_type = 'track')
    track_name = spotify.get_track_name(result)
    track_id = spotify.get_a_track_id(result)
    return track_name

# put the data in a model
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    track_name = DB.Column(DB.String(25))
    track_id = DB.Column(DB.String(25))

    def __repr__(self):
        return f'Track name: f{self.track_name} ---- Track id: f{self.track_id}'

def refresh():
    '''
    pull fresh data from spotify and refresh the database
    '''
    DB.drop_all()
    DB.create_all()

    test_name = song_info()

    print(new_record.track_name)
    print(new_record.track_id)
    print(new_record)

    DB.session.commit()
    return 'Now that is some fresh data'