# Spotify to YouTube Playlist Converter

This is a Python script that takes a Spotify playlist and creates a corresponding YouTube playlist.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.6+
- Pip: Python's package installer. Comes pre-installed with Python in most cases.

You also need the following Python packages which can be installed via pip:

- Google Client Library
- Spotipy

To install these packages, you can run the following command in your terminal:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib spotipy
```

## Setup

Before you can run the script, you'll need to set up Developer Applications for both Spotify and YouTube (Google).

### Setting up the Spotify Developer Application:

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
2. Click on 'Create an App'. Fill in the name and description of the app. Agree to the terms and conditions and click 'Create'.
3. Once the app is created, you'll be redirected to the app's page where you can find your `Client ID` and `Client Secret`.
4. Click on 'Edit Settings', add `http://localhost:8080` to the 'Redirect URIs' and click on 'Save'.

### Setting up the YouTube Developer Application:

1. Visit the [Google Cloud Console](https://console.cloud.google.com/) and log in with your Google account.
2. Create a new project by clicking on the project drop-down and clicking the 'New Project' button on the top right of the modal.
3. Once the project is created, enable the YouTube Data API for the project:
   - Go to 'Library' and search for 'YouTube Data API v3'.
   - Click on the API and then click 'Enable'.
4. Create credentials for the API:
   - Go to 'Credentials', click 'Create Credentials' and choose 'OAuth client ID'.
   - Configure the 'OAuth consent screen' as required.
   - For 'Application type', choose 'Web application'.
   - Set the 'Authorized JavaScript origins' to `http://localhost:8080`.
   - Set the 'Authorized redirect URIs' to `http://localhost:8080`.
   - Click 'Create'.

Once you've set up your applications, note down the `Client ID` and `Client Secret` for both.

## Configuration

Create a `spotify_credentials.json` file in the project directory, and include your Spotify credentials:

```json
{
	"SPOTIFY_CLIENT_ID": "<your_spotify_client_id>",
	"SPOTIFY_CLIENT_SECRET": "<your_spotify_client_secret>"
}
```

Replace `<your_spotify_client_id>` and `<your_spotify_client_secret>` with the respective values you got from your Spotify Developer Application.

Next, place your YouTube API client secret JSON file (the one you downloaded from the Google Cloud Console) in the project directory. Rename it to `client_secret_YOUTUBE.json`.

## Running the Script

To run the script, navigate to the project directory in your terminal and run:

```bash
python new.py
```

You'll be prompted to input your Spotify playlist URL. Once you provide it, the script will begin creating a private YouTube playlist with the same name and description as the Spotify playlist, and add the songs from the Spotify playlist to the YouTube playlist.

The script will print out the progress and any issues encountered during the process.

If you run into quota issues with the YouTube Data API, you may need to request a quota increase from the [Google Cloud Console](https://console.cloud.google.com/).

That's it! Enjoy your newly created YouTube playlist!
