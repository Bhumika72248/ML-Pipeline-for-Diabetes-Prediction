import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from dataclasses import dataclass
print("This is data_ingestion.py")


@dataclass
class DataIngestionConfig:

    train_data_path = os.path.join("artifacts", "train.csv")

    test_data_path = os.path.join("artifacts", "test.csv")

    raw_data_path = os.path.join("artifacts", "raw.csv")


class DataIngestion:

    def __init__(self):

        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        # Read the dataset
        df = pd.read_csv(os.path.join("data", "diabetes.csv"))

        # Create artifacts folder
        os.makedirs("artifacts", exist_ok=True)

        # Save raw dataset
        df.to_csv(
            self.ingestion_config.raw_data_path,
            index=False,
            header=True
        )

        # Split dataset
        train_set, test_set = train_test_split(
            df,
            test_size=0.2,
            random_state=42
        )

        # Save train dataset
        train_set.to_csv(
            self.ingestion_config.train_data_path,
            index=False,
            header=True
        )

        # Save test dataset
        test_set.to_csv(
            self.ingestion_config.test_data_path,
            index=False,
            header=True
        )

        return (
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path
        )


if __name__ == "__main__":

    obj = DataIngestion()

    train_path, test_path = obj.initiate_data_ingestion()

    print("Train File :", train_path)

    print("Test File  :", test_path)