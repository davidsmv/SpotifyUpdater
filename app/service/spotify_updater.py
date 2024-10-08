import json
import os
import boto3
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyUpdater:
    def __init__(self) -> None:
        pass

    def get_secret(self):
        secret_name = os.environ['SECRET_NAME']
        region_name = os.environ['AWS_REGION']

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            raise e

        # Decrypts secret using the associated KMS key
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)

    def get_spotify_instance(self, credentials):
        sp_oauth = SpotifyOAuth(
            client_id=credentials["SPOTIPY_CLIENT_ID"],
            client_secret=credentials["SPOTIPY_CLIENT_SECRET"],
            redirect_uri="http://127.0.0.1:8080/",
            scope="user-top-read playlist-modify-public",
        )
        token_info = sp_oauth.refresh_access_token(credentials["SPOTIPY_REFRESH_TOKEN"])
        access_token = token_info["access_token"]
        return spotipy.Spotify(auth=access_token)

    def update_playlist(self):
        # Get Spotify credentials from Secrets Manager
        credentials = self.get_secret()

        spotify = self.get_spotify_instance(credentials)

        # Your logic to create/modify the playlist
        list_of_songs = []
        top_tracks = spotify.current_user_top_tracks(limit=50, time_range="short_term")
        for item in top_tracks["items"]:
            list_of_songs.append(item["uri"])

        playlist_id = credentials["SPOTIFY_PLAYLIST_ID"]
        spotify.playlist_replace_items(playlist_id, list_of_songs)

        return {
            "statusCode": 200,
            "body": json.dumps("Playlist updated successfully!")
        }
