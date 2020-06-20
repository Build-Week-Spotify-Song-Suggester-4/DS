# takes the user's input (song, gets its track id and audio features, then adds it to a DB)
from pprint import pprint
from flask import Flask, Blueprint, render_template, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from web_app.services.pulldata import sp
from web_app.services.models import Track
import json
import time
import sys

#user_input_route=Blueprint("user_input_route", __name__) #not sure if we need this yet

APP = Flask(__name__)
migrate = Migrate()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
db = SQLAlchemy(APP)
db.init_app(APP)
migrate.init_app(APP,db)

#@user_input_route.route("/<track_id>")
def get_track_features():

    search_str = """N'SYNC bye bye bye """ #NEED TO INTERFACE WITH FRONT END TO GET THE USER INPUT
    # run search query and return top result only (if usery query is 'ARTIST SONG' this will work)
    result = sp.search(q=search_str, type='track', limit=1)
    pprint(result)
    #print(type(result)) ->dict
    track_id = result['tracks']['items'][0]['id']
    #print(type(track_id)) ->string
    pprint(track_id)

    start = time.time()
    #get audio features for given track
    features = sp.audio_features(track_id)
    delta = time.time() - start
    print(json.dumps(features, indent=4))
    print("features retrieved in %.2f seconds" % (delta,))

    #add user queried track to database:
    db_track = Track()
    db_track.id = features[0]['id']
    db_track.instrumentalness = features[0]['instrumentalness']
    db_track.liveness = features[0]['liveness']
    db_track.loudness = features[0]['loudness']
    db_track.mode = features[0]['mode']
    db_track.speechiness = features[0]['speechiness']
    db_track.tempo = features[0]['tempo']
    db_track.time_signature = features[0]['time_signature']
    db_track.track_href = features[0]['track_href']
    db_track.type = features[0]['type']
    db_track.valence = features[0]['valence']
    db_track.energy = features[0]['energy']
    db_track.danceability = features[0]['danceability']
    db_track.duration_ms = features[0]['duration_ms']
    db_track.acousticness =features[0]['acousticness']
    db.session.add(db_track)
    print(db_track)
    print("________________")
    db.session.commit()
    return "User Track added to DB"




