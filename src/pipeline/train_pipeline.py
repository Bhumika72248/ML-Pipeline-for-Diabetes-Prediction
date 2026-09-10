import sys

from src.exception import CustomException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainingPipeline:

    def __init__(self):
        pass

    def run_pipeline(self):

        try:

            logging.info("========== Training Pipeline Started ==========")

            # Data Ingestion
            data_ingestion = DataIngestion()

            data_ingestion.initiate_data_ingestion()

            logging.info(
                "Data Ingestion completed successfully"
            )

            # Data Validation
            data_validation = DataValidation()

            validation_status = (
                data_validation.initiate_data_validation()
            )

            if not validation_status:

                logging.error(
                    "Data Validation failed. "
                    "Training pipeline stopped."
                )

                raise ValueError(
                    "Data Validation failed"
                )

            logging.info(
                "Data Validation completed successfully"
            )

            # Data Transformation
            data_transformation = DataTransformation()

            X_train, X_test, y_train, y_test = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Data Transformation completed successfully"
            )

            # Model Training
            model_trainer = ModelTrainer()

            best_model_name, best_cv_f1 = (
                model_trainer.initiate_model_trainer(
                    X_train,
                    y_train,
                    X_test,
                    y_test
                )
            )

            logging.info(
                f"Model Training completed successfully. "
                f"Best Model: {best_model_name}, "
                f"CV F1: {best_cv_f1:.4f}"
            )

            logging.info(
                "========== Training Pipeline Completed =========="
            )

        except Exception as e:

            raise CustomException(e, sys)


if __name__ == "__main__":

    training_pipeline = TrainingPipeline()

    training_pipeline.run_pipeline()