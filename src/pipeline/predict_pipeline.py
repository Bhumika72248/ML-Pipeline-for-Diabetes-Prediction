import os
import sys
import joblib
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import replace_zero_with_nan

class PredictPipeline:

    def __init__(self):

        self.model_path = os.path.join(
            "artifacts",
            "model.pkl"
        )

        self.preprocessor_path = os.path.join(
            "artifacts",
            "preprocessor.pkl"
        )

    def predict(self, features):

        try:

            logging.info("Prediction started")

            preprocessor = joblib.load(self.preprocessor_path)
            model = joblib.load(self.model_path)

            logging.info("Preprocessor and model loaded successfully")

            features = replace_zero_with_nan(features)

            data_scaled = preprocessor.transform(features)

            prediction = model.predict(data_scaled)
 
            logging.info("Prediction completed successfully")

            return prediction

        except Exception as e:

            raise CustomException(e, sys)


class CustomData:

    def __init__(
        self,
        Pregnancies,
        Glucose,
        BloodPressure,
        SkinThickness,
        Insulin,
        BMI,
        DiabetesPedigreeFunction,
        Age
    ):

        self.Pregnancies = Pregnancies
        self.Glucose = Glucose
        self.BloodPressure = BloodPressure
        self.SkinThickness = SkinThickness
        self.Insulin = Insulin
        self.BMI = BMI
        self.DiabetesPedigreeFunction = DiabetesPedigreeFunction
        self.Age = Age

    def get_data_as_data_frame(self):

        try:

            custom_data_input_dict = {
                "Pregnancies": [self.Pregnancies],
                "Glucose": [self.Glucose],
                "BloodPressure": [self.BloodPressure],
                "SkinThickness": [self.SkinThickness],
                "Insulin": [self.Insulin],
                "BMI": [self.BMI],
                "DiabetesPedigreeFunction": [self.DiabetesPedigreeFunction],
                "Age": [self.Age]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:

            raise CustomException(e, sys)

if __name__ == "__main__":

    custom_data = CustomData(
        Pregnancies=2,
        Glucose=120,
        BloodPressure=70,
        SkinThickness=25,
        Insulin=100,
        BMI=30.5,
        DiabetesPedigreeFunction=0.5,
        Age=35
    )

    input_data = custom_data.get_data_as_data_frame()

    print("Input Data:")
    print(input_data)

    predict_pipeline = PredictPipeline()

    prediction = predict_pipeline.predict(input_data)

    print("Prediction:", prediction)