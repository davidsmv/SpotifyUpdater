# SpotifyUpdater

# Spotify Playlist Updater Lambda

This repository contains the code for an AWS Lambda function that automatically updates a Spotify playlist based on the most recently listened-to tracks. The function is designed to run periodically (e.g., every other day) using AWS EventBridge to trigger the update.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)
- [License](#license)

## Overview

The `Spotify Playlist Updater` Lambda function:
- Retrieves the user's most recently listened-to tracks on Spotify.
- Updates a specified playlist with these tracks.

The function uses Spotify's API, with credentials securely stored in AWS Secrets Manager. It also relies on AWS services like Lambda and EventBridge to automate the process.

## Prerequisites

Before deploying and running this Lambda function, you'll need:

1. **AWS Account**: To create and manage the Lambda function, Secrets Manager, and EventBridge rules.
2. **Spotify Developer Account**: To obtain the necessary API credentials.
3. **Python Environment**: To install dependencies and package the Lambda function.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/davidsmv/SpotifyUpdater.git
cd spotify-playlist-updater
```

### 2. Install Dependencies

To install the necessary Python dependencies, create a folder and run:

```bash
mkdir spotify_lambda
cd spotify_lambda
pip install -r ../requirements.txt -t .
```

This command installs the dependencies listed in `requirements.txt` into the current directory (`.`), making them ready for deployment with AWS Lambda.

### 3. Obtain Spotify API Credentials

You need to have the following Spotify API credentials:
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REFRESH_TOKEN`

You can generate the `SPOTIPY_REFRESH_TOKEN` using the `get_refresh_token.py` script provided in this repository.

### 4. Store Credentials in AWS Secrets Manager

Save the following secrets in AWS Secrets Manager under the secret name `spotify/credentials`:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REFRESH_TOKEN`
- `SPOTIFY_PLAYLIST_ID`
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`

Ensure that these secrets are stored securely, as they are critical for the function's operation.

## Configuration

### Lambda Function

The main function is located in `lambda_function.py`. It consists of the following components:

- **`get_secret()`**: Retrieves secrets from AWS Secrets Manager.
- **`get_spotify_instance()`**: Authenticates with the Spotify API using the credentials stored in Secrets Manager.
- **`lambda_handler()`**: The entry point for the Lambda function, which retrieves the latest tracks and updates the specified playlist.

### AWS Configuration

- **Secrets Manager**: Ensure your Spotify API credentials and AWS credentials are securely stored in Secrets Manager.
- **EventBridge Rule**: Set up an EventBridge rule to trigger the Lambda function on a regular schedule (e.g., every other day).

## Deployment

### 1. Package the Lambda Function

After installing the dependencies and placing `lambda_function.py` in the `spotify_lambda` directory, package the function:

```bash
zip -r9 ../spotify_lambda.zip .
```

### 2. Deploy to AWS Lambda

- Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
- Create a new Lambda function.
- Choose "Upload from" and select "Zip file" to upload `spotify_lambda.zip`.
- Set the handler to `lambda_function.lambda_handler`.
- Attach the necessary IAM role with permissions to access Secrets Manager and other required AWS services.

### 3. Set Up EventBridge

Create an EventBridge rule to trigger the Lambda function at your desired frequency (e.g., every other day). This will automate the playlist update process.

## Testing

To test the Lambda function:

1. **Manually Trigger the Lambda**: You can manually trigger the Lambda function from the AWS Lambda console to ensure it works correctly.
2. **Check CloudWatch Logs**: Monitor the logs in CloudWatch to verify the function's execution and troubleshoot any issues.
3. **Verify Spotify Playlist**: After running the function, check the Spotify playlist to ensure it has been updated as expected.
