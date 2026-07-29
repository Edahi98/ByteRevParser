import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faList } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { NewPhrasesFileField } from '../molecules/NewPhrasesFileField'
import { PredictionsDistributionChart } from '../molecules/PredictionsDistributionChart'
import { PredictionsTable } from '../molecules/PredictionsTable'

export function BatchClassifyForm({ onSubmit, isLoading, predictions, error, quickArchive }) {
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
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <FormSection
        title="Clasifica muchas frases de un jalón"
        icon={<FontAwesomeIcon icon={faList} />}
        accent="teal"
        subtitle="Elige tu modelo entrenado y sube un CSV con varias frases para ubicarlas todas en sus grupos"
      >
        <ArtifactsFileField
          fileName={artifactsFile?.name}
          onChange={(event) => setArtifactsFile(event.target.files[0] ?? null)}
          quickArchive={quickArchive}
          onUseQuickArchive={handleUseQuickArchive}
        />
        <NewPhrasesFileField fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />

        <div className="pt-2 md:w-56">
          <Button type="submit" variant="green" disabled={!artifactsFile || !file || isLoading}>
            {isLoading ? 'Clasificando...' : 'Clasificar frases'}
          </Button>
        </div>

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}

        {predictions && predictions.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 items-start">
            <PredictionsDistributionChart predictions={predictions} />
            <PredictionsTable predictions={predictions} />
          </div>
        )}
      </FormSection>
    </form>
  )
}
