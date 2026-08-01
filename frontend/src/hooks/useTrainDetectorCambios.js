import { useState } from 'react'
import JSZip from 'jszip'
import { TRAIN_DETECTOR_CAMBIOS_URL } from '../data/apiConfig'

export function useTrainDetectorCambios() {
  const [report, setReport] = useState(null)
  const [archive, setArchive] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const train = async () => {
    setIsLoading(true)
    setError(null)
    setReport(null)
    setArchive(null)

    try {
      const response = await fetch(TRAIN_DETECTOR_CAMBIOS_URL, { method: 'POST' })

      if (!response.ok) {
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || 'Error al analizar las frases')
      }

      const blob = await response.blob()
      const zip = await JSZip.loadAsync(blob)
      const reportText = await zip.file('reporte.json').async('string')

      setReport(JSON.parse(reportText))
      setArchive({ blob, filename: 'control_cambios.zip' })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { train, report, archive, error, isLoading }
}
