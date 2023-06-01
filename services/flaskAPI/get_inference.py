""" Get inference from SetFit model """
from typing import List
import pickle

sf = pickle.load(open('setfit-reddit-suomi-2022-2023.pkl', 'rb'))

print(sf)

def get_inference(data: List[str]):
    '''
    call model prediction
    '''
    preds = sf(data)
    return preds.tolist()


print(get_inference(['Hi mom']))
