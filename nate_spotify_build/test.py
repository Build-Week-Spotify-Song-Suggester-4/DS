from spotify_api import SpotifyAPI

client_id = '1efa46aff77347859b690fa4329ee6a1'
client_secret = '42e1c54ccba84332be2ef25987466119'

spotify = SpotifyAPI(client_id, client_secret)

# search a song by an artist
print('enter a song title and push enter')
song_title = input()
print('who sings this song?')
artist = input()

result = spotify.search(query = {'track': f"{song_title}", 'artist': f"{artist}"}, search_type = 'track')
'''
# it will pull up to 20 songs that are close to it
# the first song is the song most similar to our search
track_ids = spotify.get_track_ids(result)
print('1__________________________________________')
'''
# we can also get the track names from the initial search
track_name = spotify.get_track_name(result)
print('2_________________________________________')


# this will allow us to pull the first track's (the most relevant track's) id
a_track_id = spotify.get_a_track_id(result)
print('3______________________________________________')

# this track id will allow us to get audio features for a track

#print(track_ids)
#print(track_names)
print(a_track_id)
print(spotify.get_track(a_track_id))
print('4____________________________________')
print(spotify.get_audio_features(a_track_id))

