from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
 
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

class DiabetesInput(BaseModel):
    
    Pregnancies: int = Field(ge=0)
    Glucose: int = Field(gt=0)
    BloodPressure: int = Field(gt=0)
    SkinThickness: int = Field(ge=0)
    Insulin: int = Field(ge=0)
    BMI: float = Field(gt=0)
    DiabetesPedigreeFunction: float = Field(ge=0)
    Age: int = Field(gt=0)

app = FastAPI(
    title="Diabetes Prediction API",
    description="Machine Learning API for diabetes prediction",
    version="1.0.0"
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(data: DiabetesInput):

    custom_data = CustomData(
        Pregnancies=data.Pregnancies,
        Glucose=data.Glucose,
        BloodPressure=data.BloodPressure,
        SkinThickness=data.SkinThickness,
        Insulin=data.Insulin,
        BMI=data.BMI,
        DiabetesPedigreeFunction=data.DiabetesPedigreeFunction,
        Age=data.Age
    )

    input_data = custom_data.get_data_as_data_frame()

    predict_pipeline = PredictPipeline()

    prediction = predict_pipeline.predict(input_data)

    prediction_value = int(prediction[0])

    result = (
        "Diabetes predicted"
        if prediction_value == 1
        else "No diabetes predicted"
    )

    return {
        "prediction": prediction_value,
        "result": result
    }