import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTag, faStar, faCircleQuestion } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { PhraseField } from '../molecules/PhraseField'
import { UNKNOWN_LABEL } from '../../data/chartTheme'

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
        subtitle="Elige tu modelo entrenado y escribe una frase para ver a qué grupo se parece más"
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

        {result && result.etiqueta === UNKNOWN_LABEL && (
          <div className="inline-flex items-center gap-2.5 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 w-fit">
            <FontAwesomeIcon icon={faCircleQuestion} className="text-slate-400" />
            <span className="text-sm text-slate-600">
              No estoy segura de "<strong className="font-semibold">{result.frase}</strong>" — no se parece a ningún grupo conocido
            </span>
          </div>
        )}

        {result && result.etiqueta !== UNKNOWN_LABEL && (
          <div className="flex flex-col gap-2 bg-gradient-to-r from-emerald-50 to-teal-50 border border-teal-200/80 rounded-xl px-4 py-3 w-fit">
            <div className="inline-flex items-center gap-2.5">
              <FontAwesomeIcon icon={faStar} className="text-emerald-500" />
              <span className="text-sm text-slate-700">
                "<strong className="font-semibold">{result.frase}</strong>" pertenece a
              </span>
              <span className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                {result.etiqueta}
              </span>
              <span className="text-xs text-slate-500">({Math.round(result.confianza * 100)}% confianza)</span>
            </div>
            {result.terminos_clave?.length > 0 && (
              <p className="text-xs text-slate-500">
                Fragmentos característicos de ese grupo: {result.terminos_clave.join(', ')}
              </p>
            )}
          </div>
        )}
      </FormSection>
    </form>
  )
}
