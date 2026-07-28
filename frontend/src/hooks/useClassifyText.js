import { useState } from 'react'
import { CLASSIFY_TEXT_URL } from '../data/apiConfig'

export function useClassifyText() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const classify = async ({ phrase, artifactsFile }) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('phrase', phrase)
      formData.append('artifacts', artifactsFile)

      const response = await fetch(CLASSIFY_TEXT_URL, { method: 'POST', body: formData })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Error al clasificar la frase')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { classify, result, error, isLoading }
}
