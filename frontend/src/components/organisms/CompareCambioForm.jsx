import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faStar, faCircleQuestion } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { PhraseField } from '../molecules/PhraseField'

export function CompareCambioForm({ onSubmit, isLoading, result, error, quickArchive }) {
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
    <form onSubmit={handleSubmit}>
      <GradientCard icon={<FontAwesomeIcon icon={faMagnifyingGlass} />} title="Probar una frase" gradient="violet">
        <ArtifactsFileField
          accent="violet"
          fileName={artifactsFile?.name}
          onChange={(event) => setArtifactsFile(event.target.files[0] ?? null)}
          quickArchive={quickArchive}
          onUseQuickArchive={handleUseQuickArchive}
        />
        <PhraseField value={phrase} onChange={(event) => setPhrase(event.target.value)} accent="violet" />

        <Button type="submit" variant="violet" disabled={!artifactsFile || !phrase.trim() || isLoading}>
          {isLoading ? 'Comparando...' : 'Comparar'}
        </Button>

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}

        {result && !result.es_conocida && (
          <div className="inline-flex items-center gap-2.5 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 w-fit">
            <FontAwesomeIcon icon={faCircleQuestion} className="text-slate-400" />
            <span className="text-sm text-slate-600">
              "<strong className="font-semibold">{result.frase}</strong>" no es un cambio
            </span>
          </div>
        )}

        {result && result.es_conocida && (
          <div className="flex flex-col gap-2 bg-gradient-to-r from-violet-50 to-fuchsia-50 border border-violet-200/80 rounded-xl px-4 py-3 w-fit">
            <div className="inline-flex items-center gap-2.5">
              <FontAwesomeIcon icon={faStar} className="text-violet-500" />
              <span className="text-sm text-slate-700">
                "<strong className="font-semibold">{result.frase}</strong>" ya la conoce
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Se parece a: "<strong className="font-medium">{result.frase_mas_parecida}</strong>"
            </p>
          </div>
        )}
      </GradientCard>
    </form>
  )
}
