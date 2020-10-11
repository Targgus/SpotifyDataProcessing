import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import config

try:
    print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
    # Quick start code goes here

    # create a container
    blob_service_client = BlobServiceClient.from_connection_string(config.conn_str)
    container_name = "quickstart" + str(uuid.uuid4())
    container_client = blob_service_client.create_container(container_name)

    # name of the file that will live in the blob
    local_file_name = 'upload.json'

    # upload blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    with open('test_upload.json', 'rb') as data:
        blob_client.upload_blob(data)


except Exception as ex:
    print('Exception:')
    print(ex)