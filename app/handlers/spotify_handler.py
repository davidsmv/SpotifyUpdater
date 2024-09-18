from app.service.spotify_updater import SpotifyUpdater

def lambda_handler(event, context):
    # Instantiate your class
    updater  = SpotifyUpdater()

    # Call the method inside the class
    response = updater.update_playlist()

    return response