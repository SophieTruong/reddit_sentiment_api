"""
Setting up default connector to Azure: 
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli#authenticate-to-azure-and-authorize-access-to-blob-data
"""
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

def create_blob_downloader():
    '''
    TO BE RUN ONCES
    https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli#authenticate-to-azure-and-authorize-access-to-blob-data
    '''
    try:
        print("Azure Blob Storage Python quickstart sample")
        account_url = "https://mlmodelstorev0.blob.core.windows.net"
        default_credential = DefaultAzureCredential()
        print(default_credential)
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        print(blob_service_client)
        local_file = os.getenv('LOCALFILENAME')
        container_name = os.getenv('CONTAINERNAME')
        blob_name = os.getenv('BLOBNAME')
        # Download blob from Azure 
        container_client = blob_service_client.get_container_client(container= container_name) 
        print("\nDownloading blob to \n\t" + local_file)
        with open(file=local_file, mode="wb") as download_file:
            download_file.write(
                container_client.download_blob(
                blob=blob_name
                ).readall())
    
    except Exception as e:
        print(e)
        return e
create_blob_downloader()