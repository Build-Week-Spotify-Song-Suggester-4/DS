
import os
from pprint import pprint
from dotenv import load_dotenv
import spotipy
import sys
import json
load_dotenv()
from spotipy.oauth2 import SpotifyClientCredentials

#setting the credentials
client_credentials_manager = SpotifyClientCredentials(client_id = os.getenv("client_id"), 
client_secret= os.getenv("client_secret"))

#instantiating the spotipy library to connect with the API
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = True

#returns track_id for a given song, when searched in the following manner:
search_str = """N'SYNC bye bye bye """

result = sp.search(q=search_str, type='track', limit=1)
pprint(result)
#print(type(result)) ->dict
track_id = result['tracks']['items'][0]['id']
#print(type(track_id)) ->string
pprint(track_id)



#returns catalog data for any search string search_str of: album, track, artist,playlist
#any_search_str = #ENTER ANY SEARCH TERM HERE
#any_result = sp.search(q=any_search_str, type = 'track','album','artist','playlist')
#pprint.pprint(any_result)