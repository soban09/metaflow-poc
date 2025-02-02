from flask import Flask, request
import pandas as pd
import numpy as np
from datetime import datetime
import pickle, os, json

# Initialize Flask app
app = Flask(__name__)

class RandomForrest:
    def __init__(self):
        self.model = None

    def load(self):
        latest_model_path = None
        max_date = None

        for folder in os.listdir('./model'):
            if os.path.isdir(os.path.join('./model', folder)):
                datestr = folder.split('v')[1]
                date = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
                if (max_date is None) or (date > max_date):
                    max_date = date
                    latest_model_path = folder
        
        if latest_model_path is None:
            raise("No model folder was found, please train a mode first!")
        
        self.model_dir_path = os.path.join('./model', latest_model_path)
        pickle_file_path = os.path.join('./model', latest_model_path, 'model.pkl')

        with open(pickle_file_path, 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

        print("Latest Model Loaded : ", pickle_file_path)


    def log_data(self, data):
        log_file_path = os.path.join(self.model_dir_path, 'log.json')
        if os.path.exists(log_file_path):
            # If the file exists, append to it
            with open(log_file_path, 'r+') as f:
                logs = json.load(f)
                logs.append(data)
                f.seek(0)
                json.dump(logs, f, indent=4)
        else:
            # If the file doesn't exist, create a new file and write the data
            with open(log_file_path, 'w') as f:
                json.dump([data], f, indent=4)


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

    randomForrest.log_data({
        "request": payload,
        "response": res,
        "time" : datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    })
    
    return "Patient is " + res

if __name__ == '__main__':
    randomForrest.load()
    app.run(host='0.0.0.0', port=5000)