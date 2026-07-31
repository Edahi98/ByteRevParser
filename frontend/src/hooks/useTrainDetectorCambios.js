import { useState } from 'react'
import JSZip from 'jszip'
import {
  TRAIN_DETECTOR_CAMBIOS_URL,
  TRAIN_DETECTOR_CAMBIOS_STATUS_URL,
  TRAIN_DETECTOR_CAMBIOS_DOWNLOAD_URL,
} from '../data/apiConfig'

const INTERVALO_CONSULTA_MS = 2000

export function useTrainDetectorCambios() {
  const [report, setReport] = useState(null)
  const [archive, setArchive] = useState(null)
  const [progress, setProgress] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const esperarResultado = () => {
    return new Promise((resolve, reject) => {
      const intervalo = setInterval(async () => {
        try {
          const response = await fetch(TRAIN_DETECTOR_CAMBIOS_STATUS_URL)
          const estado = await response.json()
          setProgress(estado)

          if (estado.estado === 'listo') {
            clearInterval(intervalo)
            const zipResponse = await fetch(TRAIN_DETECTOR_CAMBIOS_DOWNLOAD_URL)
            const blob = await zipResponse.blob()
            const zip = await JSZip.loadAsync(blob)
            const reportText = await zip.file('reporte.json').async('string')

            setReport(JSON.parse(reportText))
            setArchive({ blob, filename: 'control_cambios.zip' })
            resolve()
          } else if (estado.estado === 'error') {
            clearInterval(intervalo)
            reject(new Error(estado.error || 'Error al analizar las frases'))
          }
        } catch (err) {
          clearInterval(intervalo)
          reject(err)
        }
      }, INTERVALO_CONSULTA_MS)
    })
  }

  const train = async () => {
    setIsLoading(true)
    setError(null)
    setReport(null)
    setArchive(null)
    setProgress(null)

    try {
      const response = await fetch(TRAIN_DETECTOR_CAMBIOS_URL, { method: 'POST' })

      if (!response.ok) {
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || 'Error al analizar las frases')
      }

      await esperarResultado()
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return { train, report, archive, progress, error, isLoading }
}
