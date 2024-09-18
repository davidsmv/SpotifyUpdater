# SpotifyUpdater

This repository contains the code for an AWS Lambda function that automatically updates a Spotify playlist based on the most recently listened-to tracks. The function is built and deployed using the AWS Serverless Application Model (SAM) and interacts with the Spotify API.

## **Table of Contents**

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Deployment](#setup-and-deployment)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. AWS Configuration](#3-aws-configuration)
  - [4. Spotify API Credentials](#4-spotify-api-credentials)
  - [5. Build and Deploy](#5-build-and-deploy)
- [Local Testing](#local-testing)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## **Introduction**

This project automates the process of updating a Spotify playlist with the latest top tracks. It uses AWS Lambda for serverless execution and is scheduled to run every other day using Amazon EventBridge (formerly CloudWatch Events).

## **Features**

- **Automated Playlist Updates**: Refreshes your Spotify playlist with new tracks every other day.
- **Serverless Architecture**: Built using AWS Lambda and AWS SAM for scalable and cost-effective deployment.
- **Secure Credential Management**: Uses AWS Secrets Manager to securely store and access Spotify API credentials.
- **Configurable Schedule**: The update frequency can be adjusted via the AWS SAM template.

## **Architecture**

1. **AWS Lambda Function**: Executes the Python script to update the Spotify playlist.
2. **Amazon EventBridge**: Triggers the Lambda function based on a specified cron schedule.
3. **AWS Secrets Manager**: Securely stores Spotify API credentials.
4. **Spotify API**: The Lambda function interacts with Spotify's API to update the playlist.

## **Prerequisites**

- **AWS Account**: An active AWS account with permissions to create Lambda functions, EventBridge rules, and access Secrets Manager.
- **AWS CLI**: Installed and configured with your AWS credentials.
- **AWS SAM CLI**: Installed on your local machine. [Install the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- **Docker**: Installed and running for local testing. [Get Docker](https://docs.docker.com/get-docker/)
- **Spotify Account**: A Spotify account with the necessary permissions to create and modify playlists.
- **Spotify Developer Application**: Created in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) to obtain API credentials.

## **Setup and Deployment**

### **1. Clone the Repository**

```bash
git clone https://github.com/davidsmv/SpotifyUpdater.git
cd SpotifyUpdater
```

### **2. Install Dependencies**

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### **3. AWS Configuration**

Ensure your AWS CLI is configured with the necessary credentials:

```bash
aws configure
```

- **AWS Access Key ID**
- **AWS Secret Access Key**
- **Default region name**: e.g., `us-east-1`


### **4. Spotify API Credentials**

### 3. Obtain Spotify API Credentials

You need to have the following Spotify API credentials:
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REFRESH_TOKEN`
- `SPOTIFY_PLAYLIST_ID`


#### **a. Create a Spotify Developer Application**

- Log in to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
- Create a new application to obtain the **Client ID** and **Client Secret**.

#### **b. Obtain a Refresh Token**

- You can generate the `SPOTIPY_REFRESH_TOKEN` using the `app/service/get_refresh_token.py` script provided in this repository.

#### **c. Store Credentials in AWS Secrets Manager**

Create a secret in AWS Secrets Manager with the following key-value pairs:

- **SPOTIPY_CLIENT_ID**: Your Spotify Client ID.
- **SPOTIPY_CLIENT_SECRET**: Your Spotify Client Secret.
- **SPOTIPY_REFRESH_TOKEN**: Your Spotify Refresh Token.
- **SPOTIFY_PLAYLIST_ID**: The ID of the Spotify playlist you want to update.

**AWS CLI Command to Create the Secret:**

```bash
aws secretsmanager create-secret \
    --name spotify/credentials \
    --secret-string '{"SPOTIPY_CLIENT_ID":"your-client-id","SPOTIPY_CLIENT_SECRET":"your-client-secret","SPOTIPY_REFRESH_TOKEN":"your-refresh-token","SPOTIFY_PLAYLIST_ID":"your-playlist-id"}' \
    --region us-east-1
```

### **5. Build and Deploy**

#### **a. Build the Application**

```bash
sam build
```

#### **b. Deploy the Application**

Use the guided deployment to configure parameters:

```bash
sam deploy --guided
```

During the guided deployment:

- **Stack Name**: `spotify-playlist-updater-stack` (or your preferred name)
- **AWS Region**: `us-east-1` (ensure it matches where your secret is stored)
- **Parameter SecretName**: `spotify/credentials` (the name of your secret)
- **Confirm changes before deploy**: `N`
- **Allow SAM CLI IAM role creation**: `Y`
- **Save arguments to samconfig.toml**: `Y`

## **Local Testing**

To test the function locally before deployment:

1. **Create a Test Event File**

   Create `event.json` with the following content:

   ```json
   {}
   ```

2. **Invoke the Function Locally**

   ```bash
   sam local invoke SpotifyUpdateFunction -e event.json
   ```

   Ensure Docker is running, as SAM CLI uses it to simulate the Lambda environment.

## **Project Structure**

```
SpotifyUpdater/
├── app/
│   ├── handlers/
│   │   ├── spotify_handler.py
│   |── service/
│   │   │── get_refresh_token.py
│   │   │── spotify_updater.py
│   ├── __init__.py
├── template.yaml
├── requirements.txt
├── README.md
├── .gitignore
```

- **app/**: Contains the Lambda function code and dependencies.
- **handlers/**: Contains the `spotify_handler.py` script with the `lambda_handler` funtion.
- **service/**: Contains the `get_refresh_token.py` to get the refresh token neccesary to update the playlist and `spotify_updater.py` class that handles the entire process, called by `lambda_handler`
- **template.yaml**: AWS SAM template defining the serverless application.
- **requirements.txt**: Lists Python dependencies.
- **README.md**: Project documentation.
- **.gitignore**: Specifies files and directories to ignore in version control.

## **Usage**

Once deployed, the Lambda function will automatically run every other day at midnight (Bogota, Colombia time) to update your Spotify playlist.

## **Troubleshooting**

- **Deployment Errors**: Ensure your AWS credentials have the necessary permissions and that all parameters are correctly specified during deployment.
- **Access Denied Errors**: Verify that the IAM role associated with your Lambda function has the required permissions to access AWS Secrets Manager.
- **Invalid Spotify Credentials**: Double-check the credentials stored in AWS Secrets Manager for accuracy.
- **Function Not Triggering**: Confirm that the EventBridge rule is correctly configured and enabled.

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## **License**

This project is licensed under the [MIT License](LICENSE).
