import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBrain } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { ModelNameField } from '../molecules/ModelNameField'
import { DatasetFileField } from '../molecules/DatasetFileField'
import { ModelParamsPanel } from '../molecules/ModelParamsPanel'
import { DEFAULT_MODEL_PARAMS } from '../../data/modelParamsDefaults'

export function TrainClassifierForm({ onSubmit, isLoading, error }) {
  const [file, setFile] = useState(null)
  const [modelName, setModelName] = useState('')
  const [params, setParams] = useState(DEFAULT_MODEL_PARAMS)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!file) return
    onSubmit({ file, modelName, params })
  }

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <FormSection
        title="Descubre grupos en tus textos"
        icon={<FontAwesomeIcon icon={faBrain} />}
        accent="emerald"
        subtitle="Sube tus frases y una red neuronal descubre sola qué grupos hay entre ellas, sin que tú las clasifiques primero. Como entrena una red de verdad, puede tardar uno o varios minutos según cuántas frases subas."
      >
        <ModelNameField value={modelName} onChange={(event) => setModelName(event.target.value)} />
        <DatasetFileField fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />
        <ModelParamsPanel params={params} onChange={setParams} />

        <div className="pt-2 md:w-72">
          <Button type="submit" variant="green" disabled={!file || isLoading}>
            {isLoading ? (
              <span className="inline-flex items-center justify-center gap-2">
                <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Entrenando tu modelo...
              </span>
            ) : (
              'Entrenar mi modelo'
            )}
          </Button>
        </div>

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}
      </FormSection>
    </form>
  )
}
