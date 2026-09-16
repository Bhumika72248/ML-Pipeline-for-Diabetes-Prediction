import { useEffect, useState } from 'react'
import './App.css'
import { predictDiabetes, checkHealth } from './services/api'

function App() {

  const [formData, setFormData] = useState({
    Pregnancies: '',
    Glucose: '',
    BloodPressure: '',
    SkinThickness: '',
    Insulin: '',
    BMI: '',
    DiabetesPedigreeFunction: '',
    Age: ''
  })

  useEffect(() => {
    const checkBackend = async () => {
      try {
        await checkHealth()
        setBackendOnline(true)
      } catch {
        setBackendOnline(false)
      }
    }

    checkBackend()
  }, [])


  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [backendOnline, setBackendOnline] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target

    setFormData({
      ...formData,
      [name]: value
    })

    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (Object.values(formData).some(value => value === '')) {
      setError('Please fill in all fields before predicting.')
      return
    }
    if (
      Number(formData.Pregnancies) < 0 ||
      Number(formData.Glucose) <= 0 ||
      Number(formData.BloodPressure) <= 0 ||
      Number(formData.BMI) <= 0 ||
      Number(formData.Age) <= 0
    ) {
      setError('Please enter valid values for all fields.')
      return
    }
    setLoading(true)
    setError('')
    setPrediction(null)

    try {
      const data = await predictDiabetes({
        Pregnancies: Number(formData.Pregnancies),
        Glucose: Number(formData.Glucose),
        BloodPressure: Number(formData.BloodPressure),
        SkinThickness: Number(formData.SkinThickness),
        Insulin: Number(formData.Insulin),
        BMI: Number(formData.BMI),
        DiabetesPedigreeFunction: Number(
          formData.DiabetesPedigreeFunction
        ),
        Age: Number(formData.Age)
      })

      setPrediction(data)

    } catch (error) {

      console.error("Prediction Error:", error)

      setError(
        'Unable to get prediction. Please make sure the backend is running.'
      )

    } finally {

      setLoading(false)

    }
  }

  const handleReset = () => {
    setFormData({
      Pregnancies: '',
      Glucose: '',
      BloodPressure: '',
      SkinThickness: '',
      Insulin: '',
      BMI: '',
      DiabetesPedigreeFunction: '',
      Age: ''
    })

    setPrediction(null)
    setError('')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Diabetes Prediction</h1>
        <p>
          Machine Learning Based Diabetes Risk Prediction
        </p>
      </header>

      <main className="main">
        <section className="prediction-card">

          <h2>Enter Patient Information</h2>

          <p className="description">
            Enter the required health-related values to generate
            a prediction from the trained machine learning model.
          </p>

          <div className={backendOnline ? 'backend-status online' : 'backend-status offline'}>
            <span className="status-dot"></span>
            {backendOnline ? 'Backend Online' : 'Backend Offline'}
          </div>

          <form className="form-container" onSubmit={handleSubmit}>

            <div className="form-group">
              <label>Pregnancies</label>

              <input
                type="number"
                name="Pregnancies"
                min="0"
                placeholder="Enter number of pregnancies"
                value={formData.Pregnancies}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Glucose</label>
              <input
                type="number"
                name="Glucose"
                min="1"
                placeholder="Enter glucose level"
                value={formData.Glucose}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Blood Pressure</label>
              <input
                type="number"
                name="BloodPressure"
                min="1"
                placeholder="Enter blood pressure"
                value={formData.BloodPressure}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Skin Thickness</label>
              <input
                type="number"
                name="SkinThickness"
                min="0"
                placeholder="Enter skin thickness"
                value={formData.SkinThickness}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Insulin</label>
              <input
                type="number"
                name="Insulin"
                min="0"
                placeholder="Enter insulin level"
                value={formData.Insulin}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>BMI</label>
              <input
                type="number"
                name="BMI"
                min="0.1"
                step="0.1"
                placeholder="Enter BMI"
                value={formData.BMI}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Diabetes Pedigree Function</label>
              <input
                type="number"
                name="DiabetesPedigreeFunction"
                min="0"
                step="0.001"
                placeholder="Enter pedigree function"
                value={formData.DiabetesPedigreeFunction}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                name="Age"
                min="1"
                placeholder="Enter age"
                value={formData.Age}
                onChange={handleInputChange}
                required
              />
            </div>

            <button
              type="submit"
              className="predict-button"
              disabled={loading}
            >
              {loading ? 'Predicting...' : 'Predict'}
            </button>

            <button
              type="button"
              className="reset-button"
              onClick={handleReset}
            >
              Reset
            </button>

          </form>

          {error && (
            <div className="error-container">
              <p>{error}</p>
            </div>
          )}

          {prediction && (
            <div
              className={
                prediction.prediction === 1
                  ? 'result-container positive'
                  : 'result-container negative'
              }
            >
              <h3>Prediction Result</h3>
              <p>
                {prediction.prediction === 1
                  ? 'Higher diabetes risk predicted by the model'
                  : 'Lower diabetes risk predicted by the model'}
              </p>
            </div>
          )}
          <p className="disclaimer">
            This prediction is generated by a machine learning model
            and is intended for educational purposes only. It should not
            be considered a medical diagnosis.
          </p>

        </section>
      </main>
    </div>
  )
}

export default App