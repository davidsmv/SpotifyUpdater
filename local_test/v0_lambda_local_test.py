# from pickle import TRUE
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util



scope = "user-top-read"
redirect_uri = "http://127.0.0.1:8080/" 
# redirect_uri = "http://localhost/"


# token =  SpotifyOAuth(scope=scope, username=username)

# spotifyObject = spotipy.Spotify(auth_manager=token)

#create playlist
# playlist_name = input("Enter playlist name: ")
# playlist_description = input("Enter playlist description: ")

# spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)




token = util.prompt_for_user_token(username = username,
                                   scope = "user-top-read",
                                   client_id= client_id,
                                   client_secret=client_secret,
                                    redirect_uri=redirect_uri
                                )

spotify = spotipy.Spotify(auth=token)
spotify.trace = True
spotify.trace_out = True

list_of_songs = []

top_tracks = spotify.current_user_top_tracks(limit=50, time_range="short_term")
for i, item in enumerate(top_tracks['items']):
    list_of_songs.append(item['uri'])

# print(top_tracks['items'][1]['uri'])
#print(list_of_songs)
# print(json.dumps(top_tracks, indent=4))

#add songs to playlist
token = util.prompt_for_user_token(username = username,
                                   scope = "playlist-modify-public",
                                   client_id= client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

spotify = spotipy.Spotify(auth=token)
spotify.trace = True
spotify.trace_out = True
playlist_id = ""




spotify.playlist_replace_items(playlist_id, list_of_songs)