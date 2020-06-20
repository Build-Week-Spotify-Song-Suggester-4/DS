import requests
import base64
import datetime
from urllib.parse import urlencode

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    # set client_id and client_secret in a .env file
    client_id = '1efa46aff77347859b690fa4329ee6a1'
    client_secret = '42e1c54ccba84332be2ef25987466119'
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

    #def get_track(self, _id):
     #   return self.get_resource(_id, resource_type='tracks')

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            string = 'not in range'
            return string
        print(lookup_url)
        print(r.status_code)
        return r.json()
    
    
    def search(self, query=None, operator=None, operator_query=None, search_type= 'artist'):
        '''
        perform a search with multiple arguments such as artist and track title
        use the base_search function above to return the query params from this function
        example of basic search: spotify.search(query = 'Time', search_type = 'track')
        ex of track and artist: spotify.search(query = {'track': 'Time', 'artist': 'Hans Zimmer'}, search_type = 'track')
         '''
        if query == None:
            raise Exception('A query is required')
        if isinstance(query, dict):
            query = ' '.join([f"{k}:{v}" for k,v in query.items()])
        if operator!= None and operator_query != None:
            if operator.lower() == 'or' or operator.lower() == 'not':
                operator = operator.upper
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
    
    def get_track_ids(self, track_dict):
        '''
        returns the id of the track 
        '''
        if type(track_dict) != dict:
            raise Exception('Please input a dictionary')
        track_ids = []
        counter = 0
        for x in track_dict['tracks']['items']:
            track_id = track_dict['tracks']['items'][counter]['id']
            print(type(track_id))
            print(track_id)
            counter = counter + 1
        return track_ids, counter
    
    def get_a_track_id(self, track_dict):
        '''
        returns the id of a track 
        '''
        if type(track_dict) != dict:
            raise Exception('Please input a dictionary')
        track_id = track_dict['tracks']['items'][0]['id']
        print(track_id)
        return track_id
    
    def get_track_name(self, track_dict):
        '''
        returns the names of the tracks
        '''
        if type(track_dict) != dict:
            raise Exception('Please input a dictionary')
        track_name = track_dict['tracks']['items'][0]['name']
        print(track_name)
        return track_name

    '''
    # while this code worked, I found a better way to refactor it using the 
    # get_resource() function from above

    def get_track(self, _id):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/tracks"
        lookup_url = f"{endpoint}/{_id}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            string = 'not in range'
            return string
        print(lookup_url)
        print(r.status_code)
        return r.json()
    '''

    # get_track refactored using other functions from the class
    def get_track(self, _id):
        return self.get_resource(_id, resource_type='tracks')

    def get_audio_features(self, _id):
        return self.get_resource(_id, resource_type='audio-features')

    
