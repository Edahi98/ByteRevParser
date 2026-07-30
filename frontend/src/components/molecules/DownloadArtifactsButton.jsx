import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDownload } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'

export function DownloadArtifactsButton({ archive }) {
  const handleDownload = () => {
    const url = URL.createObjectURL(archive.blob)
    const link = document.createElement('a')
    link.href = url
    link.download = archive.filename
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <Button variant="green" onClick={handleDownload}>
      <span className="inline-flex items-center justify-center gap-2">
        <FontAwesomeIcon icon={faDownload} /> Descargar detector
      </span>
    </Button>
  )
}
