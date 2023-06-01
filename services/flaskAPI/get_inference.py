""" Get inference from SetFit model """
from typing import List
import pickle
import pathlib
from azure.storage.blob import BlobServiceClient
import time 
import os
from dotenv import load_dotenv

load_dotenv()

STORAGEACCOUNTURL= os.getenv('STORAGEACCOUNTURL')
STORAGEACCOUNTKEY=  os.getenv('STORAGEACCOUNTKEY')
LOCALFILENAME=  os.getenv('LOCALFILENAME')
CONTAINERNAME=  os.getenv('CONTAINERNAME')
BLOBNAME=  os.getenv('BLOBNAME')

#download from blob
t1=time.time()
blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, AzureSasCredential=STORAGEACCOUNTKEY)
blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, BLOBNAME, snapshot=None)
with open(LOCALFILENAME, "wb") as my_blob:
    blob_data = blob_client_instance.download_blob()
    blob_data.readinto(my_blob)
t2=time.time()
print(("It takes %s seconds to download "+BLOBNAME) % (t2 - t1))


sf = pickle.load(open('setfit-reddit-suomi-2022-2023.pickle', 'rb'))


def get_inference(data: List[str]):
    '''
    call model prediction
    '''
    preds = sf(data)
    return preds.tolist()


print(get_inference(['Hi mom']))
