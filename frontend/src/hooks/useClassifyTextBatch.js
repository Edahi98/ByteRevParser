import { useState } from 'react'
import { CLASSIFY_TEXT_BATCH_URL } from '../data/apiConfig'

export function useClassifyTextBatch() {
  const [predictions, setPredictions] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const classifyBatch = async ({ file, artifactsFile }) => {
    setIsLoading(true)
    setError(null)
    setPredictions(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('artifacts', artifactsFile)

      const response = await fetch(CLASSIFY_TEXT_BATCH_URL, { method: 'POST', body: formData })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Error al clasificar las frases')
      }

      setPredictions(data.predicciones)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { classifyBatch, predictions, error, isLoading }
}
