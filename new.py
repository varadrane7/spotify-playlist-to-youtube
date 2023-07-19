import spotipy
from spotipy.oauth2 import SpotifyOAuth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import urlparse
import json

# Load credentials from JSON
with open('spotify_credentials.json') as json_file:
    credentials = json.load(json_file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials['SPOTIFY_CLIENT_ID'],
                                               client_secret=credentials['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri="http://localhost/",
                                               scope="playlist-read-private"))

spotify_playlist_url = input("Enter Spotify playlist URL: ")  # Receive input from user
spotify_playlist_id = urlparse(spotify_playlist_url).path.split('/')[-1]

results = sp.playlist(spotify_playlist_id)

spotify_playlist_name = results['name']
spotify_playlist_description = results['description']

track_details = []
for item in results['tracks']['items']:
    track = item['track']
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    track_details.append((track_name, artist_name))

print(f"Found {len(track_details)} tracks in Spotify playlist.")

# Initialize YouTube client
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secret_YOUTUBE.json", scopes)
credentials = flow.run_local_server(port=8080)

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

request = youtube.playlists().insert(
    part="snippet,status",
    body={
      "snippet": {
        "title": spotify_playlist_name,
        "description": spotify_playlist_description,
        "tags": [
          "Spotify",
          "Playlist"
        ],
        "defaultLanguage": "en"
      },
      "status": {
        "privacyStatus": "private"  # Changed privacy status to private
      }
    }
)

response = request.execute()
playlist_id = response['id']

print(f"Created YouTube playlist with ID: {playlist_id}")

# Search for tracks and add to playlist
for track_name, artist_name in track_details:
    try:
        print(f"Processing track: {track_name} by {artist_name}")
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=f"{track_name} {artist_name} -lyrics"
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": video_id
                }
              }
            }
        )
        response = request.execute()
        print(f"Added track to YouTube playlist: {track_name} by {artist_name}")
    except googleapiclient.errors.HttpError as error:
        print(f"Could not add track to YouTube playlist: {track_name} by {artist_name}. Error: {error}")
