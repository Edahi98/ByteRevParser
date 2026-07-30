import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faListCheck } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { NewPhrasesFileField } from '../molecules/NewPhrasesFileField'
import { CambioResultsTable } from '../molecules/CambioResultsTable'

export function CompareCambioBatchForm({ onSubmit, isLoading, resultados, error, quickArchive }) {
  const [artifactsFile, setArtifactsFile] = useState(null)
  const [file, setFile] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!artifactsFile || !file) return
    onSubmit({ file, artifactsFile })
  }

  const handleUseQuickArchive = () => {
    setArtifactsFile(new File([quickArchive.blob], quickArchive.filename, { type: 'application/zip' }))
  }

  return (
    <form onSubmit={handleSubmit}>
      <GradientCard icon={<FontAwesomeIcon icon={faListCheck} />} title="Comparar varias" gradient="amber">
        <ArtifactsFileField
          accent="amber"
          fileName={artifactsFile?.name}
          onChange={(event) => setArtifactsFile(event.target.files[0] ?? null)}
          quickArchive={quickArchive}
          onUseQuickArchive={handleUseQuickArchive}
        />
        <NewPhrasesFileField accent="amber" fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />

        <Button type="submit" variant="amber" disabled={!artifactsFile || !file || isLoading}>
          {isLoading ? 'Comparando...' : 'Comparar'}
        </Button>

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}

        {resultados && resultados.length > 0 && <CambioResultsTable resultados={resultados} />}
      </GradientCard>
    </form>
  )
}
