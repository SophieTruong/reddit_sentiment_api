"""
Handle app routing logic
"""
import os
import pandas as pd
import datetime

from flask import Flask, request, jsonify, Response, flash, redirect
from flask_cors import CORS, cross_origin

from get_inference import get_inference
from utils import get_uuid_id

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def index():
    """ This is the main flask route """
    if request.method == 'POST':
        try:
            inp = request.get_json()
            print(inp)
            inference = get_inference([inp])
            print(inference[0])
            inference_translated = 'negative' if inference[0] == 1 else 'positive/neutral'
            data = {
                'id': inp['id'],
                'text': inp['text'],
                'sentiment': inference_translated,
                'created_at': datetime.datetime.now()
            }
            save_to_db([data])
            return jsonify(data)
        # Server error handling
        except Exception:  # pylint: disable=broad-except
            return Response(
                "Wrong type of input data. Only submit text from text area.",
                status=400,
            )
    else:
        try:
            data = pd.read_csv('db.csv')
            return jsonify(data.sentiment.value_counts().to_dict())
        except Exception:  # pylint: disable=broad-except
            return Response(
                "No data were found",
                status=400,
            )
    return 'Hello, World'


@app.route("/file_submit", methods=['POST'])
@cross_origin()
def upload_file():
    try:
        # check if the post request has the file part
        if 'fileName' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get('fileName')
        df = pd.read_csv(file, encoding="ISO8859_15",
                         engine='python', on_bad_lines='skip',
                         encoding_errors='backslashreplace')
        print('Uploaded df: ', df)
        inference = get_inference(df.text.to_list())
        df['id'] = [get_uuid_id() for i in df['text'].to_list()]
        df['sentiment'] = inference
        df['sentiment'].replace(
            {0: 'neutral/positive', 1: 'negative'}, inplace=True)
        df['created_at'] = [datetime.datetime.now()
                            for i in df['text'].to_list()]
        print('DF:', df)
        print('DF:', df.id)
        data = df.to_dict('records')
        save_to_db(data)
        return jsonify(data)
    except Exception:  # pylint: disable=broad-except
        return Response(
            "Wrong type of input file. Only submit CSV file.", status=400,
        )


@app.route('/update_sentiment/<id>', methods=['PUT'])
@cross_origin()
def updateOne(id):
    print(id)
    inp = request.get_json()
    data = pd.read_csv('db.csv')
    data.loc[data.id == id, 'sentiment'] = inp['sentiment']
    data.loc[data.id == id, 'create_at'] = datetime.datetime.now()
    print(data.loc[data.id == id])
    data.to_csv('db.csv', index=False)
    return jsonify(data.loc[data.id == id].to_dict('records'))


def save_to_db(data):
    data_df = pd.DataFrame(data)
    if os.path.exists('db.csv'):
        df = pd.read_csv('db.csv')
        df = pd.concat([df, data_df]).reset_index(drop=True)
        print(df)
        df.to_csv('db.csv', index=False)
        # must be text column, else error
    else:
        data_df.to_csv('db.csv', index=False)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
