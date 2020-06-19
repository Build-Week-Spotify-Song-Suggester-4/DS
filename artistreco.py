# return a recommended artist based on Spotify API's feature tracks, and an input of artist name
import argparse
import logging
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

#setting the credentials
client_credentials_manager = SpotifyClientCredentials(client_id = os.getenv("client_id"), 
client_secret= os.getenv("client_secret"))
#instantiating the spotipy library to connect with the API
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = True

logger = logging.getLogger('examples.artist_recommendations')
logging.basicConfig(level='INFO')


def get_args():
    parser = argparse.ArgumentParser(description='Recommendations for the '
                                     'given artist')
    parser.add_argument('-a', '--artist', required=True, help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    results = sp.recommendations(seed_artists=[artist['id']])
    for track in results['tracks']:
        logger.info('Recommendation: %s - %s', track['name'],
                    track['artists'][0]['name'])


def main():
    args = get_args()
    artist = get_artist(args.artist)
    if artist:
        show_recommendations_for_artist(artist)
    else:
        logger.error(f"Can't find that artist: {args.artist}") #,args.artist)


if __name__ == '__main__':
    main()