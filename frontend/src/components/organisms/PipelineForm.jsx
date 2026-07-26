import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileLines } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { FormSection } from '../molecules/FormSection'
import { FileField } from '../molecules/FileField'
import { SchemaBuilderField } from '../molecules/SchemaBuilderField'
import { DeveloperModeToggle } from '../molecules/DeveloperModeToggle'
import { pipelineModes } from '../../data/pipelineModes'
import { samplePipelineJson } from '../../data/samplePipeline'
import { useFileText } from '../../hooks/useFileText'

export function PipelineForm({ onSubmit, isLoading, children }) {
  const [file, setFile] = useState(null)
  const [simpleFields, setSimpleFields] = useState(['Versión', 'Fecha de revisión', 'Elaboró'])
  const [pipeline, setPipeline] = useState(samplePipelineJson)
  const [mode, setMode] = useState(pipelineModes[0].value)
  const [useSchema, setUseSchema] = useState(true)
  const [schema, setSchema] = useState('')
  const [query, setQuery] = useState('')
  const [topK, setTopK] = useState('')
  const [isDevMode, setIsDevMode] = useState(false)

  const loadPipelineFromFile = useFileText(setPipeline)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!file) return

    let finalSchema = null

    if (useSchema) {
      if (schema && schema.trim().length > 0) {
        finalSchema = schema.trim()
      } else {
        const validFields = simpleFields.map((f) => f.trim()).filter((f) => f.length > 0)

        if (validFields.length > 0) {
          const schemaObj = {}
          validFields.forEach((fieldName) => {
            schemaObj[fieldName] = ''
          })
          finalSchema = JSON.stringify(schemaObj, null, 2)
        }
      }
    }

    onSubmit({
      file,
      pipeline,
      mode: mode || pipelineModes[0].value,
      query: query || null,
      topK: query ? topK || null : null,
      schema: finalSchema,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <FormSection
        title="Extrae el control de cambios de tu documento"
        icon={<FontAwesomeIcon icon={faFileLines} />}
        accent="blue"
        subtitle="Sube tu documento y dinos qué datos del control de cambios necesitas obtener"
      >
        <FileField accent="blue" fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />
        <SchemaBuilderField accent="blue" fields={simpleFields} onChange={setSimpleFields} />
      </FormSection>

      <section className="w-full py-8 bg-slate-100/80 border-t border-b border-slate-200/70">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex flex-col items-start gap-4">
          <div className="w-full md:w-auto md:min-w-[260px]">
            <Button type="submit" disabled={!file || isLoading}>
              {isLoading ? (
                <span className="inline-flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Extrayendo control de cambios...
                </span>
              ) : (
                'Extraer control de cambios'
              )}
            </Button>
          </div>

          <DeveloperModeToggle isOpen={isDevMode} onToggle={() => setIsDevMode(!isDevMode)} />
        </div>
      </section>

      {isDevMode &&
        children({
          pipeline,
          onPipelineChange: (event) => setPipeline(event.target.value),
          onLoadPipelineFile: (event) => loadPipelineFromFile(event.target.files[0]),
          mode,
          onModeChange: (event) => setMode(event.target.value),
          useSchema,
          onUseSchemaChange: (event) => setUseSchema(event.target.checked),
          schema,
          onSchemaChange: (event) => setSchema(event.target.value),
          query,
          onQueryChange: (event) => setQuery(event.target.value),
          topK,
          onTopKChange: (event) => setTopK(event.target.value),
        })}
    </form>
  )
}
