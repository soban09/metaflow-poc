from metaflow import FlowSpec, step
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from datetime import datetime
import pickle, os, logging, json

# Set up logging
logger = logging.getLogger()

class MachineLearningFlow(FlowSpec):

    @step
    def start(self):
        logger.info("Machine Learning workflow started")
        print("Machine Learning workflow started")
        self.next(self.load)

    @step
    def load(self):
        #Load the dataset
        logger.info("Loading the dataset...")
        print("Loading the dataset...")

        self.data = pd.read_csv('./dataset/diabetes-dev.csv')
        
        print("Dataset loaded")
        logger.info("Dataset loaded")
        self.next(self.preprocess)

    @step
    def preprocess(self):
        # Handling missing data
        logger.info("Handling missing data...")
        print("Handling missing data...")
        print(self.data.isnull().sum())
        self.data.fillna(self.data.mean(), inplace=True)

        # Feature Scaling
        logger.info("Handling Feature Scaling...")
        print("Handling Feature Scaling...")
        scaler = StandardScaler()
        self.data[
            ['PlasmaGlucose', 
             'DiastolicBloodPressure', 
             'TricepsThickness', 
             'SerumInsulin', 
             'BMI', 
             'DiabetesPedigree', 
             'Age']
            ] = scaler.fit_transform(self.data[[
                'PlasmaGlucose', 
                'DiastolicBloodPressure', 
                'TricepsThickness', 
                'SerumInsulin', 
                'BMI', 
                'DiabetesPedigree', 
                'Age']
                ])
        
        logger.info("Handling Min-Max Scaling...")
        print("Handling Min-Max Scaling...")
        scaler = MinMaxScaler()
        self.data[[
            'PlasmaGlucose', 
            'DiastolicBloodPressure', 
            'TricepsThickness', 
            'SerumInsulin', 
            'BMI', 
            'DiabetesPedigree', 
            'Age']
            ] = scaler.fit_transform(self.data[
                ['PlasmaGlucose', 
                 'DiastolicBloodPressure', 
                 'TricepsThickness', 
                 'SerumInsulin', 
                 'BMI', 
                 'DiabetesPedigree', 
                 'Age']
                ])
        
        self.correlation_matrix = self.data.corr()
        self.next(self.split)

    @step
    def split(self):
        # Split dataset into training and test sets
        print("Splitting the dataset...")
        logger.info("Splitting the dataset...")
        
        X = self.data.drop(columns=['Diabetic', 'PatientID'])
        y = self.data['Diabetic']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.train_features = X_train
        self.test_features = X_test
        self.train_labels = y_train
        self.test_labels = y_test
        
        print("Dataset splitted")
        logger.info("Dataset splitted")
        self.next(self.train)

    @step
    def train(self):
        # Train the model
        print("Training the model...")
        logger.info("Training the model...")
        
        self.model = RandomForestClassifier()
        self.model.fit(self.train_features, self.train_labels)
        
        print("Model trained")
        logger.info("Model trained")
        self.next(self.evaluate)

    @step
    def evaluate(self):
        # Evaluate the model
        print("Evaluating the model...")
        logger.info("Evaluating the model...")

        predictions = self.model.predict(self.test_features)
        self.model_info = {
            "accuracy": accuracy_score(self.test_labels, predictions),
            "precision": precision_score(self.test_labels, predictions),
            "recall": recall_score(self.test_labels, predictions),
            "f1_score": f1_score(self.test_labels, predictions),
            "confusion_matrix": confusion_matrix(self.test_labels, predictions).tolist()
        }

        print(f"Evaluated. Model accuracy: {self.model_info['accuracy']}")
        logger.info(f"Evaluated. Model accuracy: {self.model_info['accuracy']}")
        self.next(self.save)

    @step
    def save(self):
        # saving the new model
        print("Saving the model...")
        logger.info("Saving the model...")

        # Create a timestamp
        current_time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.model_info['model_version'] = "v" + current_time_stamp

        # Create model directory
        model_directory = os.path.join('model', 'diabetes_classifier_model_' + self.model_info['model_version'])
        os.makedirs(model_directory, exist_ok=True)
        self.model_info['model_path'] = os.path.join(model_directory, 'model.pkl')

        # Save the model information as a JSON file inside the same directory
        model_info_path = os.path.join(model_directory, 'model_info.json')
        with open(model_info_path, 'w') as json_file:
            json.dump(self.model_info, json_file, indent=4)

        # Save the model to the new directory
        with open(self.model_info['model_path'], 'wb') as f:
            pickle.dump(self.model, f)

        print(f"Model saved to directory {model_directory}")
        logger.info(f"Model saved to directory {model_directory}")
        self.next(self.end)

    @step
    def end(self):
        # End of flow
        print("Machine Learning workflow completed.")
        logger.info("Machine Learning workflow completed.")

if __name__ == '__main__':
    MachineLearningFlow()