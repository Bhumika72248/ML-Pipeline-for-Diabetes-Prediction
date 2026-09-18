# Diabetes Prediction ML Pipeline

An end-to-end Machine Learning application for diabetes prediction, built with Python and Scikit-learn and deployed as a full-stack web application.

The project focuses on building a structured and modular ML pipeline covering data ingestion, validation, preprocessing, model training, evaluation, prediction, API development, containerization, and cloud deployment.

---

## 🚀 Live Application

* **Frontend:** [https://ml-pipeline-for-diabetes-prediction.vercel.app/](https://ml-pipeline-for-diabetes-prediction.vercel.app/)
* **Backend API:** [https://diabetes-prediction-api-latest-9zja.onrender.com/](https://diabetes-prediction-api-latest-9zja.onrender.com/)
* **API Documentation:** [https://diabetes-prediction-api-latest-9zja.onrender.com/docs](https://diabetes-prediction-api-latest-9zja.onrender.com/docs)

---

## 📌 Project Overview

This project implements an end-to-end Machine Learning workflow for predicting diabetes based on patient-related health attributes.

Instead of only training a Machine Learning model in a notebook, the project follows a modular, production-oriented architecture.

```text
Raw Dataset
     ↓
Data Ingestion
     ↓
Data Validation
     ↓
Exploratory Data Analysis
     ↓
Data Transformation
     ↓
Model Training & Evaluation
     ↓
Trained Model
     ↓
Prediction Pipeline
     ↓
FastAPI REST API
     ↓
Docker Container
     ↓
Cloud Deployment
     ↓
React Frontend
```

---

## 🛠️ Technologies Used

| Category | Technologies |
| :--- | :--- |
| **Machine Learning** | Python, Pandas, NumPy, Scikit-learn, SciPy, Joblib |
| **Backend** | FastAPI, Pydantic, Uvicorn |
| **Frontend** | React, Vite, JavaScript, CSS |
| **DevOps & Deployment** | Docker, Docker Hub, Render, Vercel, Git & GitHub |

---

## 📂 Project Structure

```text
Diabetes Prediction/
│
├── artifacts/
│   ├── model.pkl
│   ├── preprocessor.pkl
│   ├── train.csv
│   ├── test.csv
│   ├── raw.csv
│   └── validation_status.txt
│
├── data/
│   └── diabetes.csv
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── notebook/
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/
│   │   ├── predict_pipeline.py
│   │   └── train_pipeline.py
│   │
│   ├── exception.py
│   ├── logger.py
│   ├── utils.py
│   └── __init__.py
│
├── .gitignore
├── Dockerfile
├── requirements.txt
├── app.py
├── setup.py
└── README.md
```

---

## 🔄 Machine Learning Pipeline

### 1. Data Ingestion
The `DataIngestion` component:
* Reads the raw diabetes dataset.
* Stores the raw dataset in the `artifacts/` directory.
* Splits the dataset into training (80%) and testing (20%) sets using `random_state=42` for reproducibility.
* Saves the generated datasets for downstream stages.

### 2. Data Validation
The `DataValidation` component verifies dataset integrity before processing. It checks required columns, missing values, duplicate rows, and structural correctness.

* **Expected Features:** `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`
* **Target Variable:** `Outcome`
* **Output:** Status saved to `artifacts/validation_status.txt`.

### 3. Exploratory Data Analysis
Identified feature distributions, correlations, outliers, and suspicious zero values. Certain features contain zero values that represent missing/invalid physiological measurements rather than true zeros:
* `Glucose`
* `BloodPressure`
* `SkinThickness`
* `Insulin`
* `BMI`

### 4. Data Transformation
* **Zero-Value Handling:** Converts invalid zeros to `NaN`.
* **Imputation:** Replaces missing values using median imputation.
* **Scaling:** Standardizes features using `StandardScaler`.
* **Artifact:** Preprocessing object saved to `artifacts/preprocessor.pkl`.

---

## 🤖 Model Training & Comparison

Three classification algorithms were evaluated using 5-fold cross-validation evaluated on **F1 Score**:

| Model | CV F1 Score |
| :--- | :--- |
| **Logistic Regression** | 0.6238 |
| **Decision Tree** | 0.5296 |
| **Random Forest** | **0.6284** |

**Random Forest Classifier** achieved the best performance and was selected as the production model, saved to `artifacts/model.pkl`.

---

## 🔮 Prediction Pipeline

Implemented in `src/pipeline/predict_pipeline.py`, separating prediction logic from the web framework:

```text
Input Data ➔ DataFrame ➔ Handle Zero Values ➔ Load preprocessor.pkl ➔ Transform ➔ Load model.pkl ➔ Prediction
```

---

## 🌐 FastAPI Backend

Exposes the model via REST endpoints with automated OpenAPI docs at `/docs`.

### Key Endpoints

* **Health Check:** `GET /health`
  ```json
  { "status": "healthy" }
  ```
* **Prediction:** `POST /predict`
  
  *Request:*
  ```json
  {
    "Pregnancies": 2,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 25,
    "Insulin": 100,
    "BMI": 30.5,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 35
  }
  ```
  
  *Response:*
  ```json
  {
    "prediction": 0,
    "result": "No diabetes predicted"
  }
  ```

---

## 🖥️ React Frontend

Provides a responsive UI built with React + Vite containing input forms, dynamic validation, error handling, backend health monitoring, loading feedback, and disclaimers.

---

## 🐳 Docker Containerization

### Build Image
```bash
docker build -t diabetes-prediction-api .
```

### Run Container
```bash
docker run -d --name diabetes-api -p 8000:8000 diabetes-prediction-api
```

---

## ☁️ Deployment & Architecture

```text
                    USER
                      │
                      ▼
          ┌─────────────────────┐
          │       Vercel        │
          │   React Frontend    │
          └──────────┬──────────┘
                     │ HTTPS
                     ▼
          ┌─────────────────────┐
          │       Render        │
          │  FastAPI / Docker   │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Prediction Pipeline │
          │ Preprocessor ➔ RF   │
          └─────────────────────┘
```

* **Backend Image:** `bhumika339/diabetes-prediction-api:latest` (Render)
* **Frontend:** Hosted on Vercel

---

## 🔐 Configuration

Configured via environment variables:
* **Frontend (`.env`):** `VITE_API_URL=https://diabetes-prediction-api-latest-9zja.onrender.com`
* **Backend (`.env`):** `FRONTEND_URL=https://ml-pipeline-for-diabetes-prediction.vercel.app`

---

## ▶️ Running Locally

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn app:app --reload
```
* **API:** `http://127.0.0.1:8000`
* **Docs:** `http://127.0.0.1:8000/docs`

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
* **Frontend:** `http://localhost:5173`

---

## 🧪 Testing & Metrics

### Model Test Set Performance
* **Accuracy:** 0.7403
* **Precision:** 0.6230
* **Recall:** 0.6909
* **F1 Score:** 0.6552

> **Note:** Test set performance metrics are specific to this evaluation setup and should not be used as clinical indicators.

---

## 🔄 CI/CD Automation (Future Roadmap)

To transition from manual deployment to automated workflows, continuous integration and continuous deployment can be configured via GitHub Actions.

```text
                    Developer
                        │
                        │ git push
                        ▼
                     GitHub
                        │
                        ▼
                GitHub Actions
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
         Run Tests            Docker Build
             │                     │
             └──────────┬──────────┘
                        ▼
                     SUCCESS
                        │
                        ▼
                    Deployment
                        │
               ┌────────┴────────┐
               ▼                 ▼
            Render            Vercel
```

---

## ⚠️ Disclaimer

This application is strictly for **educational and demonstration purposes**. Predictions are machine learning outputs and should **not** be considered medical diagnoses or substitutes for professional healthcare evaluation.

---

## 👩‍💻 Author

**Bhumika Sahu**  
*B.Tech – Data Science*  
* [GitHub](https://github.com/Bhumika72248)
* [LinkedIn](https://www.linkedin.com/in/bhumika-sahu-0170a329)