#TODO
"""
Get Spotify music data for currently liked tracks
Form JSON object
Send file to Cosmos DB
Schedule process with Airflow
Transform data somehow
Present results in Power BI
"""

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
results = sp.current_user_saved_tracks(limit=50)

# blob client
container_name = 'spotifycurrentsavedtracks' + str(uuid.uuid4())
blob_service_client = BlobServiceClient.from_connection_string(config.conn_str)
# container_name = "quickstart" + str(uuid.uuid4())
container_client = blob_service_client.create_container(container_name)

track_info = []
for i, item in enumerate(results['items']):
    track = item['track']
    # print(track['name'] + ' - ' + track['artists'][0]['name'])
    trackID = results['items'][i]['track']['id']
    # print(trackID)

    update_track = {}
    update_track['key'] = i
    update_track['track_name'] = results['items'][i]['track']['name']
    update_track['track_artist'] = results['items'][i]['track']['artists'][0]['name']
    update_track['track_analysis'] =  sp.audio_features(trackID)

    # track_info.append(update_track)

    # print(update_track)

    local_file_name = results['items'][i]['track']['name']
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    
    with open('test_upload.json', 'w') as outfile:
        json.dump(update_track, outfile)    

    with open('test_upload.json', 'rb') as data:
        blob_client.upload_blob(data)


# print(json.dumps(track_info, indent=4))