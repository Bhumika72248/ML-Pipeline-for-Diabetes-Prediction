'''
DataTransformationConfig
DataTransformation
train/test loading
feature-target separation
numerical feature selection
suspicious-zero handling
SimpleImputer
StandardScaler
Pipeline
ColumnTransformer
fit_transform()
transform()
prevention of test-data leakage
NumPy transformed arrays
joblib
serialization
preprocessor.pkl
loading the saved preprocessor

'''
import os
import sys
import joblib

import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import replace_zero_with_nan


@dataclass
class DataTransformationConfig:

    preprocessor_obj_file_path = os.path.join(
        "artifacts",
        "preprocessor.pkl"
    )

class DataTransformation:

    def __init__(self):

        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self):

        try:

            train_df = pd.read_csv("artifacts/train.csv")
            test_df = pd.read_csv("artifacts/test.csv")

            logging.info("Train and test datasets read successfully")

            X_train = train_df.drop(columns=["Outcome"])
            y_train = train_df["Outcome"]

            X_test = test_df.drop(columns=["Outcome"])
            y_test = test_df["Outcome"]

            X_train = replace_zero_with_nan(X_train)
            X_test = replace_zero_with_nan(X_test)
            
            numerical_features = [
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age"
            ]

            
            numerical_pipeline = Pipeline(
                 steps=[
                      ("imputer", SimpleImputer(strategy="median")),
                      ("scaler", StandardScaler())
                 ]
            )

            preprocessor = ColumnTransformer(
                    transformers=[
                            ("num", numerical_pipeline, numerical_features)
                        ]
            )

        
            X_train_transformed = preprocessor.fit_transform(X_train)

            X_test_transformed = preprocessor.transform(X_test)

            logging.info("Data transformation completed successfully")

            joblib.dump(
                preprocessor,
                self.data_transformation_config.preprocessor_obj_file_path
            )

            logging.info("Preprocessor object saved successfully")

            return X_train_transformed, X_test_transformed, y_train, y_test

        except Exception as e:

            raise CustomException(e, sys)

if __name__ == "__main__":

    data_transformation = DataTransformation()

    X_train_transformed, X_test_transformed, y_train, y_test = (
        data_transformation.initiate_data_transformation()
    )

    print("Data Transformation completed successfully.")