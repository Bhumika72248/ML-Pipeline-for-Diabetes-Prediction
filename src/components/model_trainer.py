import os
import sys

import pandas as pd

import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import cross_val_score

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation

@dataclass
class ModelTrainerConfig:

    trained_model_file_path = os.path.join(
        "artifacts",
        "model.pkl"
    )


class ModelTrainer:

    def __init__(self):

        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(
        self,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        try:

            model = LogisticRegression(max_iter=1000)

            decision_tree = DecisionTreeClassifier(
                random_state=42
            )

            random_forest = RandomForestClassifier(
                n_estimators=100,
                random_state=42
             )

            models = {
                "Logistic Regression": model,
                "Decision Tree": decision_tree,
                "Random Forest": random_forest
            }

            results = {}

            for model_name, model in models.items():

                logging.info(f"Training {model_name}")

                cv_scores = cross_val_score(
                    model,
                    X_train,
                    y_train,
                    cv=5,
                    scoring="f1"
                )

                cv_f1 = cv_scores.mean()
                logging.info(
                    f"{model_name} Cross-Validation F1: {cv_f1:.4f}"
                )

                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)

                results[model_name] = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "cv_f1": cv_f1
                }

                logging.info(
                    f"{model_name} - "
                    f"Accuracy: {accuracy:.4f}, "
                    f"Precision: {precision:.4f}, "
                    f"Recall: {recall:.4f}, "
                    f"F1: {f1:.4f}"
                )

            best_model_name = max(
                results,
                key=lambda name: results[name]["cv_f1"]
            )

            best_model = models[best_model_name]

            best_cv_f1 = results[best_model_name]["cv_f1"]

            logging.info(
                f"Best Model: {best_model_name}"
            )

            logging.info(
                f"Best Cross-Validation F1: {best_cv_f1:.4f}"
            )
            
            joblib.dump(
                best_model,
                self.model_trainer_config.trained_model_file_path
            )

            logging.info(
                f"Best model saved successfully at "
                f"{self.model_trainer_config.trained_model_file_path}"
            )
            
            return best_model_name, best_cv_f1

        except Exception as e:

            raise CustomException(e, sys)

if __name__ == "__main__":

    data_transformation = DataTransformation()

    X_train, X_test, y_train, y_test = (
        data_transformation.initiate_data_transformation()
    )

    model_trainer = ModelTrainer()

    model_trainer.initiate_model_trainer(
        X_train,
        y_train,
        X_test,
        y_test
    )
    