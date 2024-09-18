import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace these with your actual credentials
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8080/"

scope = "user-top-read playlist-modify-public"

sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope)

# This will prompt you to authenticate in the browser
token_info = sp_oauth.get_access_token(as_dict=True)

print(token_info)

# Print out the refresh token
print("Access Token:", token_info['access_token'])
print("Refresh Token:", token_info['refresh_token'])

