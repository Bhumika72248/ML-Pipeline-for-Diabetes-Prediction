const API_URL = import.meta.env.VITE_API_URL

export const predictDiabetes = async (data) => {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    throw new Error('Prediction request failed')
  }

  return await response.json()
}

export const checkHealth = async () => {
  const response = await fetch(`${API_URL}/health`)

  if (!response.ok) {
    throw new Error('Backend is not healthy')
  }

  return response.json()
}