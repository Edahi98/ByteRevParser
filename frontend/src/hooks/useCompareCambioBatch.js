import { useState } from 'react'
import { COMPARE_CAMBIO_BATCH_URL } from '../data/apiConfig'

export function useCompareCambioBatch() {
  const [resultados, setResultados] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const compareBatch = async ({ file, artifactsFile }) => {
    setIsLoading(true)
    setError(null)
    setResultados(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('artifacts', artifactsFile)

      const response = await fetch(COMPARE_CAMBIO_BATCH_URL, { method: 'POST', body: formData })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Error al comparar las frases')
      }

      setResultados(data.resultados)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { compareBatch, resultados, error, isLoading }
}
