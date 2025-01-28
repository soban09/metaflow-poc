from flask import Flask, request
import pandas as pd
import numpy as np
from datetime import datetime
import pickle, os, argparse

# Initialize Flask app
app = Flask(__name__)

class RandomForrest:
    def __init__(self):
        self.model = None

    def load(self):
        files = None
        latest_model_path = None
        max_date = None

        for folders, _, files in os.walk('./model'):
            files = files

        for file in files:
            datestr = file.split('v')[1].split('.')[0]
            date = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
            if (max_date is None) or (date > max_date):
                max_date = date
                latest_model_path = file

        model_path = os.path.join('model', latest_model_path)

        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)

        print("Latest Model Loaded : ", model_path)

randomForrest = RandomForrest()

@app.route('/test', methods=['POST'])
def recommend():

    payload = request.get_json()
    data = payload['data']
    features = payload['features']

    data = np.array([data])
    data_df = pd.DataFrame(data, columns=features)
    prediction = int(randomForrest.model.predict(data_df)[0])

    res = "Diabetic" if prediction else "Not Diabetic"
    return "Patient is " + res

if __name__ == '__main__':
    randomForrest.load()
    app.run(host='0.0.0.0', port=5000)