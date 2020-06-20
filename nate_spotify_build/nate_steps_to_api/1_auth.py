import requests
import base64
import datetime

print("begin")

client_id = '1efa46aff77347859b690fa4329ee6a1'
client_secret = '42e1c54ccba84332be2ef25987466119'
client_creds = f"{client_id}:{client_secret}"
# encodes the client_creds into base 64 
client_creds_b64 = base64.b64encode(client_creds.encode())

# do a lookup for a token
# this token is for future requests

token_url = 'https://accounts.spotify.com/api/token'
method = "POST"

token_data = {
    "grant_type": "client_credentials"}

# takes the base64 encoded client credentials from above
token_headers = {

    "Authorization": f"Basic {client_creds_b64.decode()}" # <base64 encoded client_id:client_secret>"
}

r = requests.post(token_url, data=token_data, headers=token_headers)
valid_request = r.status_code in range(200, 299)
token_response_data = r.json()

now = datetime.datetime.now()
access_token = token_response_data['access_token']
expires_in = token_response_data['expires_in'] # seconds
expires = now + datetime.timedelta(seconds=expires_in)
did_expire = expires < now

if valid_request:
    print(valid_request)
    print(r.json())
    print(client_creds_b64)
    print(client_creds)
    print('done')