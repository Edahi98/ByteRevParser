import { useState } from 'react'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { FileField } from '../molecules/FileField'
import { PipelineJsonField } from '../molecules/PipelineJsonField'
import { ModeField } from '../molecules/ModeField'
import { SchemaToggleField } from '../molecules/SchemaToggleField'
import { SchemaField } from '../molecules/SchemaField'
import { QueryField } from '../molecules/QueryField'
import { TopKField } from '../molecules/TopKField'
import { pipelineModes } from '../../data/pipelineModes'
import { samplePipelineJson } from '../../data/samplePipeline'
import { useFileText } from '../../hooks/useFileText'

export function PipelineForm({ onSubmit, isLoading }) {
  const [file, setFile] = useState(null)
  const [pipeline, setPipeline] = useState(samplePipelineJson)
  const [mode, setMode] = useState(pipelineModes[0].value)
  const [useSchema, setUseSchema] = useState(false)
  const [schema, setSchema] = useState('')
  const [query, setQuery] = useState('')
  const [topK, setTopK] = useState('')

  const loadPipelineFromFile = useFileText(setPipeline)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!file) return
    onSubmit({
      file,
      pipeline,
      mode,
      query: query || null,
      topK: query ? topK || null : null,
      schema: useSchema ? (schema || null) : null,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <FormSection
        title="Tu documento y pipeline"
        icon="📄"
        accent="blue"
        subtitle="Selecciona el archivo a procesar y revisa la configuración base del proceso"
      >
        <FileField accent="blue" fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />
        <PipelineJsonField
          accent="blue"
          value={pipeline}
          onChange={(event) => setPipeline(event.target.value)}
          onLoadFile={(event) => loadPipelineFromFile(event.target.files[0])}
        />
      </FormSection>

      <FormSection
        title="Salida"
        icon="⚙️"
        accent="indigo"
        subtitle="Configura la forma y estructura en que deseas recibir la información procesada"
      >
        <ModeField
          accent="indigo"
          value={mode}
          onChange={(event) => setMode(event.target.value)}
          options={pipelineModes}
          disabled={useSchema}
        />
        <SchemaToggleField
          accent="indigo"
          checked={useSchema}
          onChange={(event) => setUseSchema(event.target.checked)}
        />
        {useSchema && (
          <SchemaField accent="indigo" value={schema} onChange={(event) => setSchema(event.target.value)} />
        )}
      </FormSection>

      <FormSection
        title="Buscar lo más relevante (opcional)"
        icon="🔍"
        accent="cyan"
        subtitle="Filtra y ordena la información por relevancia según tus palabras clave"
      >
        <QueryField accent="cyan" value={query} onChange={(event) => setQuery(event.target.value)} />
        <TopKField
          accent="cyan"
          value={topK}
          onChange={(event) => setTopK(event.target.value)}
          disabled={!query}
        />
      </FormSection>

      <section className="w-full py-10 bg-slate-100/80 border-t border-slate-200/70">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex justify-start">
          <div className="w-full md:w-auto md:min-w-[240px]">
            <Button type="submit" disabled={!file || isLoading}>
              {isLoading ? (
                <span className="inline-flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Procesando documento...
                </span>
              ) : (
                'Ejecutar pipeline'
              )}
            </Button>
          </div>
        </div>
      </section>
    </form>
  )
}


