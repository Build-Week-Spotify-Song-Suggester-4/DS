from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from spotify_api import SpotifyAPI 

client_id = '1efa46aff77347859b690fa4329ee6a1'
client_secret = '42e1c54ccba84332be2ef25987466119'
# create a spotify api object
spotify = SpotifyAPI(client_id, client_secret)

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Chosetherite0601!@localhost/spotify'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mlgdtyguhaxygr:5403b37315ad40e35adb35a2e4d998b44bec6718ebcd4b5804a5439db7836eae@ec2-52-20-248-222.compute-1.amazonaws.com:5432/dfqe6qa9kggo1a'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create a database to house songs: view using pgadmin4
class User_songs(db.Model):
    __tablename__ = 'user_songs3'
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String)
    track_id = db.Column(db.String)
    track_name = db.Column(db.String)
    acousticness = db.Column(db.Float)
    danceability = db.Column(db.Float)
    duration_ms = db.Column(db.Float)
    energy = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    key = db.Column(db.Integer)
    liveness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    speechiness = db.Column(db.Float)
    tempo = db.Column(db.Float)
    time_signature = db.Column(db.Integer)
    valence = db.Column(db.Float)
    popularity = db.Column(db.Integer)
    
    def __init__(self, artist_name, track_id, track_name, acousticness, 
                    danceability, duration_ms, energy, instrumentalness, 
                    key, liveness, loudness, mode, speechiness, tempo, 
                    time_signature, valence, popularity):
        self.artist_name = artist_name
        self.track_id = track_id 
        self.track_name = track_name
        self.acousticness = 0
        self.danceability = danceability
        self.duration_ms = 0
        self.energy = 0
        self.instrumentalness = 0
        self.key = 0
        self.liveness = 0
        self.loudness = 0
        self.mode = 0
        self.speechiness = 0
        self.tempo = 0
        self.time_signature = 0
        self.valence = 0
        self.popularity = 0





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_index')
def test_index():
    return render_template('test_index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        track_name = request.form['track']
        artist_name = request.form['artist']
        suggestions = request.form['suggestions']
        # pull a result from spotify api using user input
        result = spotify.search(query = {'track': f"{track_name}", 'artist': f"{artist_name}"}, search_type = 'track')
        # get the track id
        track_id = spotify.get_a_track_id(result)
        # get the audio features using the track id
        audio_features = spotify.get_audio_features(track_id)
        # get the danceability in order to compare to other tracks in the database
        danceability = audio_features['danceability']
        print(artist_name, track_id, track_name, suggestions, audio_features)
        print('Danceability: ', danceability)

        # assign all other features a value
        acousticness = 0
        duration_ms = 0
        energy = 0
        instrumentalness = 0
        key = 0
        liveness = 0
        loudness = 0
        mode = 0
        speechiness = 0
        tempo = 0
        time_signature = 0
        valence = 0
        popularity = 0

        # make sure the user enters information
        if track_name == '' or artist_name == '':
            return render_template('index.html', message='Please entered required fields')

        # check to see if this track is already in the database or not
        # if there is no track with that id, put it into the database
        if db.session.query(User_songs).filter(User_songs.track_id == track_id).count() == 0:
            data = User_songs(artist_name, track_id, track_name, acousticness, 
                    danceability, duration_ms, energy, instrumentalness, 
                    key, liveness, loudness, mode, speechiness, tempo, 
                    time_signature, valence, popularity)
            db.session.add(data)
            db.session.commit()
            print(f'{track_name} has been added to the database')
            #return render_template('success.html')
            return str(db.session.query(User_songs).filter(User_songs.danceability == .9))
        # otherwise, return the success template   
        print(f'{track_name} was already in the database') 
        print(db.session.query(User_songs).filter(User_songs.danceability == .9))
        #return render_template('success.html')
        return str(db.session.query(User_songs).filter(User_songs.danceability == .9))
        



if __name__ =='__main__':
    
    app.run()

