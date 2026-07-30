import { useState } from 'react'
import { COMPARE_CAMBIO_URL } from '../data/apiConfig'

export function useCompareCambio() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const compare = async ({ phrase, artifactsFile }) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('phrase', phrase)
      formData.append('artifacts', artifactsFile)

      const response = await fetch(COMPARE_CAMBIO_URL, { method: 'POST', body: formData })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Error al comparar la frase')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { compare, result, error, isLoading }
}
