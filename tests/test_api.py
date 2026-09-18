from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_prediction():
    payload = {
        "Pregnancies": 2,
        "Glucose": 120,
        "BloodPressure": 70,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 30.5,
        "DiabetesPedigreeFunction": 0.5,
        "Age": 35
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "prediction" in result
    assert "result" in result
    assert result["prediction"] in [0, 1]

def test_invalid_prediction_input():
    payload = {
        "Pregnancies": 2,
        "Glucose": 0,
        "BloodPressure": 70,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 30.5,
        "DiabetesPedigreeFunction": 0.5,
        "Age": 35
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422