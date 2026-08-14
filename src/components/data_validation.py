import os
import sys

import pandas as pd

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataValidationConfig:

    validation_status_file_path = os.path.join(
        "artifacts",
        "validation_status.txt"
    )


class DataValidation:

    def __init__(self):

        self.data_validation_config = DataValidationConfig()

    def initiate_data_validation(self):

        try:

            logging.info("Data Validation Started")

            df = pd.read_csv("artifacts/train.csv")

            logging.info("Dataset read successfully")

            missing_values = df.isnull().sum().sum()
            duplicate_rows = df.duplicated().sum()

            logging.info(f"Dataset shape: {df.shape}")
            logging.info(f"Missing values:{missing_values}")
            logging.info(f"Duplicate rows: {duplicate_rows}")

            required_columns = [
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
                "Outcome"
            ]

            validation_status = True
            if not all(column in df.columns for column in required_columns):

                validation_status = False

                logging.warning("Required columns are missing")

            if missing_values >0:

                validation_status = False

                logging.warning("Dataset contains missing values")

            if duplicate_rows >0:

                validation_status = False

                logging.warning("Dataset contains duplicate rows")

            with open(
                self.data_validation_config.validation_status_file_path,
                "w"
            ) as file:

                file.write(f"Validation Status: {validation_status}")

            logging.info(
                f"Data Validation Status: {validation_status}"
            )

            return validation_status

        except Exception as e:

            raise CustomException(e, sys)
if __name__ == "__main__":

    data_validation = DataValidation()

    result = data_validation.initiate_data_validation()

    print("Validation Result:", result)