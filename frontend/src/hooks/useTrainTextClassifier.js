import { useState } from 'react'
import JSZip from 'jszip'
import { TRAIN_TEXT_CLASSIFIER_URL } from '../data/apiConfig'

function extractFilename(contentDisposition) {
  const match = /filename="?([^"]+)"?/.exec(contentDisposition || '')
  return match ? match[1] : 'text_classifier_artifacts.zip'
}

export function useTrainTextClassifier() {
  const [report, setReport] = useState(null)
  const [archive, setArchive] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const train = async ({ file, modelName }) => {
    setIsLoading(true)
    setError(null)
    setReport(null)
    setArchive(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      if (modelName) formData.append('model_name', modelName)

      const response = await fetch(TRAIN_TEXT_CLASSIFIER_URL, { method: 'POST', body: formData })

      if (!response.ok) {
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || 'Error al entrenar el clasificador')
      }

      const blob = await response.blob()
      const filename = extractFilename(response.headers.get('content-disposition'))
      const zip = await JSZip.loadAsync(blob)
      const reportEntry = Object.keys(zip.files).find((name) => name.endsWith('_reporte.json'))
      const reportText = await zip.file(reportEntry).async('string')

      setReport(JSON.parse(reportText))
      setArchive({ blob, filename })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { train, report, archive, error, isLoading }
}
