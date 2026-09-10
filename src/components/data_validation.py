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

            logging.info(f"Data types: \n{df.dtypes}")

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
            missing_values = df.isnull().sum().sum()
            duplicate_rows = df.duplicated().sum()

            logging.info(f"Dataset shape: {df.shape}")
            logging.info(f"Missing values:{missing_values}")
            logging.info(f"Duplicate rows: {duplicate_rows}")

            validation_status = True

            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:
                validation_status = False

                logging.warning(
                    f"Required columns are missing: {missing_columns}"
                )


            if missing_values >0:

                validation_status = False

                logging.warning("Dataset contains missing values")

            if duplicate_rows >0:

                validation_status = False

                logging.warning("Dataset contains duplicate rows")

            non_numeric_columns = [
                column
                for column in required_columns
                if column in df.columns
                and not pd.api.types.is_numeric_dtype(df[column])
            ]   

            if non_numeric_columns:
                validation_status = False

                logging.warning(
                f"Non-numeric columns found: {non_numeric_columns}"
                )


            expected_column_count = len(required_columns)

            if df.shape[1] != expected_column_count:
                validation_status = False

                logging.warning(
                    f"Unexpected number of columns. "
                    f"Expected: {expected_column_count}, "
                    f"Found: {df.shape[1]}"
                )

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