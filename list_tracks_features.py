import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import sys
import json
import config
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

token = util.prompt_for_user_token(
    config.username,
    config.scope,
    client_id=config.client_id,
    client_secret=config.client_secret, 
    redirect_uri=config.redirect_url
)

sp = spotipy.Spotify(auth=token)

# blob client
container_name = 'spotifytrackfeatures'
blob_service_client = BlobServiceClient.from_connection_string(config.conn_str)

container_client = blob_service_client.create_container(container_name)



results = sp.user_playlists(config.username, limit=50)

track_features = []
for i, item in enumerate(results['items']):
    playlist_name = item['name']
    playlist_id = item['id']

    playlist_info = {}
    playlist_info['name'] = playlist_name
    playlist_info['id'] = playlist_id

    playlist_tracks = sp.user_playlist_tracks(config.username, playlist_id)

    track_list = []
    for i, item in enumerate(playlist_tracks['items']):
        # print(item['track']['name'])
        name = item['track']['name']
        track_id = item['track']['id']
        artist = item['track']['artists'][0]['name']

        tracks = {}
        tracks['name'] = name
        tracks['id'] = track_id
        tracks['artists'] = artist
        tracks['track_analysis'] =  sp.audio_features(track_id)

        with open('track_features.json', 'w') as outfile:
            json.dump(tracks, outfile)
    
        local_file_name = f"{name}"

        blob_client = blob_service_client.get_blob_client(container=container_name, blob='track_' + str(uuid.uuid4()))
        
        with open('track_features.json', 'rb') as data:
            blob_client.upload_blob(data)




