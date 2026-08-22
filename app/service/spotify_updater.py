import json
import os

import boto3
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyUpdater:
    def __init__(self) -> None:
        pass

    def get_secret(self):
        parameter_name = os.environ['PARAMETER_NAME']
        region_name = os.environ['AWS_REGION']

        # Create an SSM Parameter Store client
        client = boto3.client(service_name="ssm", region_name=region_name)

        try:
            get_parameter_response = client.get_parameter(
                Name=parameter_name, WithDecryption=True
            )
        except Exception as e:
            print(f"Error retrieving parameter {parameter_name}: {e}")
            raise e

        # Decrypts SecureString parameter using the associated KMS key
        secret = get_parameter_response["Parameter"]["Value"]
        return json.loads(secret)

    def get_spotify_instance(self, credentials):
        sp_oauth = SpotifyOAuth(
            client_id=credentials["SPOTIPY_CLIENT_ID"],
            client_secret=credentials["SPOTIPY_CLIENT_SECRET"],
            redirect_uri="http://127.0.0.1:8080/",
            scope="user-top-read playlist-modify-public",
        )
        token_info = sp_oauth.refresh_access_token(
            credentials["SPOTIPY_REFRESH_TOKEN"]
        )
        access_token = token_info["access_token"]
        return spotipy.Spotify(auth=access_token)

    def update_playlist(self):
        # Get Spotify credentials from Secrets Manager
        credentials = self.get_secret()

        spotify = self.get_spotify_instance(credentials)

        # Your logic to create/modify the playlist
        list_of_songs = []
        top_tracks = spotify.current_user_top_tracks(
            limit=50, time_range="short_term"
        )
        for item in (top_tracks or {}).get("items", []):
            list_of_songs.append(item["uri"])

        playlist_id = credentials["SPOTIFY_PLAYLIST_ID"]
        spotify.playlist_replace_items(playlist_id, list_of_songs)

        return {
            "statusCode": 200,
            "body": json.dumps("Playlist updated successfully!")
        }
