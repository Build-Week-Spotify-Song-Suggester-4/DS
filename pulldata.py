from __future__ import print_function
import os
from flask import Flask, session, request, redirect
import spotipy
import time
import sys
import json

from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = True

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
results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
"""