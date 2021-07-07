import requests
import base64
import datetime
from urllib.parse import urlencode
import json

print("begin")

client_id = '1efa46aff77347859b690fa4329ee6a1'
client_secret = '42e1c54ccba84332be2ef25987466119'

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
   
    def get_client_creds(self):
        '''
        returns a base64 encoded string
        '''
        client_id = self.client_id
        client_secret = self.client_secret
        # check to see if there is a client_id/secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_creds()
        return {
            "Authorization": f"Basic {client_creds_b64}" # <base64 encoded client_id:client_secret>"
            }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
            }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        valid_request = r.status_code not in range(200, 299)

        if valid_request:
            raise Exception("could not authenticate client")
        
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True


    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token


    # functions that use the token to access spotify api
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def get_track(self, _id):
        return self.get_resource(_id, resource_type='track')

    def search(self, query, search_type= 'artist'):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        print(lookup_url)
        print(r.status_code)
        return r.json()

'''spotify = SpotifyAPI(client_id, client_secret)

# get the track object using the search function
track = spotify.search("Time", search_type="track")
print(track['tracks']['items'][0])
print('_______________________________________')
print(track['tracks']['items'][0]['artists'][0]['id'])
artist_id = track['tracks']['items'][0]['artists'][0]['id']
artist = spotify.get_artist(artist_id)
print('_____________________________________________')
print(artist)

print(spotify.get_artist('6fOM144jA4Sp5b9PpYCkzz'))


print('End')'''

spotify = SpotifyAPI(client_id, client_secret)

track = spotify.search("White and Nerdy", search_type="track")
print(track['tracks']['items'][0])
print('______________________________________________________')
print(track['tracks']['items'][0]['album'])

print('____________________________________________________________________')

print('album id: ', track['tracks']['items'][0]['album']['id'])
album_id = track['tracks']['items'][0]['album']['id']

print('____________________________________________________________________')

print('Track title: ', track['tracks']['items'][0]['name'])

print('____________________________________________________________________')

print('track id: ', track['tracks']['items'][1]['id'])
track_id = track['tracks']['items'][0]['id']

print('____________________________________________________________________')

print(len(track['tracks']['items']))

print('____________________________________________________________________')

print('artist id: ', track['tracks']['items'][0]['artists'][0]['id'])
artist_id = track['tracks']['items'][0]['artists'][0]['id']

artist = spotify.get_artist(artist_id)
print(artist['name'])
album = spotify.get_album(album_id)
print(album['name'])
#one_track = spotify.get_track(track_id)
#print(track)


print('End')