from fastapi import FastAPI
from pydantic import BaseModel
 
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

class DiabetesInput(BaseModel):

    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

app = FastAPI()

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