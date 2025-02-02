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
        latest_model_path = None
        model_folder_path = './model'
        max_date = None

        for folder in os.listdir(model_folder_path):
            if os.path.isdir(os.path.join(model_folder_path, folder)):
                print(folder)
                datestr = folder.split('v')[1]
                date = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
                if (max_date is None) or (date > max_date):
                    max_date = date
                    latest_model_path = folder
        
        if latest_model_path is None:
            raise("No model folder was found, please train a mode first!")

        model_path = os.path.join(model_folder_path, latest_model_path, 'model.pkl')

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