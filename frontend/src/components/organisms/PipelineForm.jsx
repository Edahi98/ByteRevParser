import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileLines, faSliders } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'
import { FileField } from '../molecules/FileField'
import { SchemaBuilderField } from '../molecules/SchemaBuilderField'
import { PipelineJsonField } from '../molecules/PipelineJsonField'
import { useFileText } from '../../hooks/useFileText'

export function PipelineForm({ onSubmit, isLoading }) {
  const [file, setFile] = useState(null)
  const [simpleFields, setSimpleFields] = useState(['Versión', 'Fecha de revisión', 'Elaboró'])
  const [pipeline, setPipeline] = useState(null)
  const [pipelineFileName, setPipelineFileName] = useState(null)

  const loadPipelineFromFile = useFileText(setPipeline)

  const handleLoadPipelineFile = (event) => {
    const selectedFile = event.target.files[0]
    if (!selectedFile) return
    setPipelineFileName(selectedFile.name)
    loadPipelineFromFile(selectedFile)
  }

  const validFields = simpleFields.map((f) => f.trim()).filter((f) => f.length > 0)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!file || !pipeline || validFields.length === 0) return

    const schemaObj = {}
    validFields.forEach((fieldName) => {
      schemaObj[fieldName] = ''
    })

    onSubmit({
      file,
      pipeline,
      schema: JSON.stringify(schemaObj, null, 2),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col">
      <div 
        className="w-full py-10 md:py-14 bg-cover bg-center bg-no-repeat bg-fixed"
        style={{
          backgroundImage: "linear-gradient(to bottom, rgba(239, 246, 255, 0.4), rgba(238, 242, 255, 0.6), rgba(255, 255, 255, 0.9)), url('/bg-detector.png')"
        }}
      >
        <div className="max-w-5xl mx-auto px-4 md:px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            {/* Card 1: Documento a procesar */}
            <GradientCard icon={<FontAwesomeIcon icon={faFileLines} />} title="Documento" gradient="blue">
              <FileField accent="blue" fileName={file?.name} onChange={(event) => setFile(event.target.files[0] ?? null)} />
              
              <div className="pt-1 mt-4 border-t border-slate-100">
                <Button type="submit" disabled={!file || !pipeline || validFields.length === 0 || isLoading}>
                  {isLoading ? (
                    <span className="inline-flex items-center justify-center gap-2">
                      <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      Extrayendo...
                    </span>
                  ) : (
                    'Extraer'
                  )}
                </Button>
              </div>
            </GradientCard>

            {/* Card 2: Configuración de Extracción */}
            <GradientCard icon={<FontAwesomeIcon icon={faSliders} />} title="Configuración" gradient="violet">
              <PipelineJsonField fileName={pipelineFileName} onLoadFile={handleLoadPipelineFile} />
              <SchemaBuilderField accent="violet" fields={simpleFields} onChange={setSimpleFields} />
            </GradientCard>
          </div>
        </div>
      </div>
    </form>
  )
}
