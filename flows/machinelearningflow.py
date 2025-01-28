from metaflow import FlowSpec, step
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from datetime import datetime
import pickle, os, logging

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
        self.accuracy = accuracy_score(self.test_labels, predictions)
        self.precision = precision_score(self.test_labels, predictions)
        self.recall = recall_score(self.test_labels, predictions)
        self.f1 = f1_score(self.test_labels, predictions)
        self.cm = confusion_matrix(self.test_labels, predictions)

        print(f"Evaluated. Model accuracy: {self.accuracy}")
        logger.info(f"Evaluated. Model accuracy: {self.accuracy}")
        self.next(self.save)

    @step
    def save(self):
        # saving the new model
        print("Saving the model...")
        logger.info("Saving the model...")

        current_time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.model_version = "v"+current_time_stamp
        self.model_path = os.path.join('model', 'diabetes_classifier_model.pkl')
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)

        print("Model saved saved to directory ./model")
        logger.info("Model saved saved to directory ./model")
        self.next(self.end)

    @step
    def end(self):
        # End of flow
        print("Machine Learning workflow completed.")
        logger.info("Machine Learning workflow completed.")

if __name__ == '__main__':
    MachineLearningFlow()