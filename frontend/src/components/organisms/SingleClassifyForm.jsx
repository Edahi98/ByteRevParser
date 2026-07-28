import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTag, faStar } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { PhraseField } from '../molecules/PhraseField'

export function SingleClassifyForm({ onSubmit, isLoading, result, error, quickArchive }) {
  const [artifactsFile, setArtifactsFile] = useState(null)
  const [phrase, setPhrase] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!artifactsFile || !phrase.trim()) return
    onSubmit({ phrase: phrase.trim(), artifactsFile })
  }

  const handleUseQuickArchive = () => {
    setArtifactsFile(new File([quickArchive.blob], quickArchive.filename, { type: 'application/zip' }))
  }

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <FormSection
        title="Prueba tu modelo con una frase"
        icon={<FontAwesomeIcon icon={faTag} />}
        accent="teal"
        subtitle="Elige tu modelo entrenado y escribe una frase para ver a qué clase la asigna"
      >
        <ArtifactsFileField
          fileName={artifactsFile?.name}
          onChange={(event) => setArtifactsFile(event.target.files[0] ?? null)}
          quickArchive={quickArchive}
          onUseQuickArchive={handleUseQuickArchive}
        />
        <PhraseField value={phrase} onChange={(event) => setPhrase(event.target.value)} />

        <div className="pt-2 md:w-56">
          <Button type="submit" variant="green" disabled={!artifactsFile || !phrase.trim() || isLoading}>
            {isLoading ? 'Clasificando...' : 'Clasificar frase'}
          </Button>
        </div>

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}

        {result && (
          <div className="inline-flex items-center gap-2.5 bg-gradient-to-r from-emerald-50 to-teal-50 border border-teal-200/80 rounded-xl px-4 py-3 w-fit">
            <FontAwesomeIcon icon={faStar} className="text-emerald-500" />
            <span className="text-sm text-slate-700">
              "<strong className="font-semibold">{result.frase}</strong>" pertenece a
            </span>
            <span className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs font-bold px-3 py-1 rounded-full">
              {result.etiqueta}
            </span>
          </div>
        )}
      </FormSection>
    </form>
  )
}
