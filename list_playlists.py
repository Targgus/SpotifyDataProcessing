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
container_name = 'spotifyuserplaylists'
blob_service_client = BlobServiceClient.from_connection_string(config.conn_str)

# container_client = blob_service_client.create_container(container_name)



results = sp.user_playlists(config.username, limit=50)

playlists = []
for i, item in enumerate(results['items']):
    name = item['name']
    playlist_id = item['id']

    playlist_info = {}
    playlist_info['name'] = name
    playlist_info['id'] = playlist_id

    playlists.append(playlist_info)

with open('playlists.json', 'w') as outfile:
    json.dump(playlists, outfile)

blob_client = blob_service_client.get_blob_client(container=container_name, blob='userplaylists')
with open('playlists.json', 'rb') as data:
    blob_client.upload_blob(data)

print(playlists)
    


# playlist_tracks = sp.user_playlist_tracks(config.username, '37i9dQZF1CyVDibakhbKKt')

# for i, item in enumerate(playlist_tracks['items']):
#     print(item['track']['name'])
#     # name = item['name']
#     # playlist_id = item['id']
#     # print(f"{name} and {playlist_id}")


