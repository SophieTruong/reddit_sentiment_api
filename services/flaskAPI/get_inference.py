""" Get inference from SetFit model """
from typing import List
import pickle
import pathlib

# current working directory
print(str(pathlib.Path().absolute()))
sf = pickle.load(open('setfit-reddit-suomi-2022-2023.pickle', 'rb'))


def get_inference(data: List[str]):
    '''
    call model prediction
    '''
    preds = sf(data)
    return preds.tolist()


print(get_inference(['Hi mom']))
