""" Get inference from SetFit model """
from typing import List
import pickle
import pathlib
import dvc.api

data = dvc.api.read(
    'setfit-reddit-suomi-2022-2023.pkl.dvc',
    repo='https://github.com/SophieTruong/reddit_sentiment_api.git',
    remote='azure',
    mode='rb'
)
model = pickle.loads(data)

# current working directory
print(str(pathlib.Path().absolute()))
# sf = pickle.load(open('setfit-reddit-suomi-2022-2023.pickle', 'rb'))


def get_inference(data: List[str]):
    '''
    call model prediction
    '''
    preds = model(data)
    return preds.tolist()


print(get_inference(['Hi mom']))
