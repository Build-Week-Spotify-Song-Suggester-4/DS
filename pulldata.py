#from __future__ import print_function
import os
from pprint import pprint
from dotenv import load_dotenv
from flask import Flask, session, request, redirect
import spotipy
import time
import sys
import json
load_dotenv()
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id = os.getenv("client_id"), 
client_secret= os.getenv("client_secret"))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = True


# code below is to pull acoustic FEATURES of tracks of a given artist. # confirmed working

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
else:
    artist_name = 'weezer'

results = sp.search(q=artist_name, limit=50)
tids = []
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
    tids.append(t['uri'])

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
for feature in features:
    print(json.dumps(feature, indent=4))
    #print()
    #analysis = sp._get(feature['analysis_url'])
    #print(json.dumps(analysis, indent=4))
    #print()
print("features retrieved in %.2f seconds" % (delta,))


# code below is to pull acoustic FEATURES of a specified track (1). # confirmed working
"""
tids='spotify:track:4TTV7EcfroSLWzXRY6gLv6'

if len(sys.argv) > 1:
    tids = sys.argv[1:]
    print(tids)

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
print(json.dumps(features, indent=4))
print("features retrieved in %.2f seconds" % (delta,))
"""


#code below is to search for songs by artist. #confirmed working
"""
results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
"""


# code below is to pull audio ANALYSIS for a given track. # confirmed working
"""
if len(sys.argv) > 1:
    tid = sys.argv[1]
else:
    tid = 'spotify:track:4TTV7EcfroSLWzXRY6gLv6'

start = time.time()
analysis = sp.audio_analysis(tid)
delta = time.time() - start
print(json.dumps(analysis, indent=4))
print("analysis retrieved in %.2f seconds" % (delta,))
"""
