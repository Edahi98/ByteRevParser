import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileLines, faRotateLeft, faSliders } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'
import { FileField } from '../molecules/FileField'
import { SchemaBuilderField } from '../molecules/SchemaBuilderField'
import { PipelineJsonField } from '../molecules/PipelineJsonField'
import { ArtifactsFileField } from '../molecules/ArtifactsFileField'
import { usePipelineForm } from '../../hooks/usePipelineForm'

export function PipelineForm({ onSubmit, isLoading }) {
  const {
    file,
    artifacts,
    pipeline,
    pipelineFileName,
    schemaFields,
    schema,
    isReady,
    isDirty,
    selectDocument,
    selectArtifacts,
    loadPipelineFile,
    changeSchemaFields,
    resetForm,
  } = usePipelineForm()

  const handleLoadPipelineFile = (event) => {
    loadPipelineFile(event.target.files[0])
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!isReady) return

    onSubmit({ file, pipeline, schema, artifacts })
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
              {/* La `key` remonta el input nativo al limpiar: sin ella conserva su
                  FileList y volver a elegir el mismo archivo no dispara `change`. */}
              <FileField
                key={file ? 'documento-cargado' : 'documento-vacio'}
                accent="blue"
                fileName={file?.name}
                onChange={(event) => selectDocument(event.target.files[0] ?? null)}
              />

              <div className="pt-1 mt-4 border-t border-slate-100 flex items-center gap-2">
                <div className="flex-1">
                  <Button type="submit" disabled={!isReady || isLoading}>
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
                <div className="shrink-0">
                  <Button variant="secondary" onClick={resetForm} disabled={!isDirty || isLoading}>
                    <span className="inline-flex items-center gap-1.5">
                      <FontAwesomeIcon icon={faRotateLeft} /> Limpiar
                    </span>
                  </Button>
                </div>
              </div>
            </GradientCard>

            {/* Card 2: Configuración de Extracción */}
            <GradientCard icon={<FontAwesomeIcon icon={faSliders} />} title="Configuración" gradient="violet">
              <PipelineJsonField
                key={pipelineFileName ? 'pipeline-cargado' : 'pipeline-vacio'}
                fileName={pipelineFileName}
                onLoadFile={handleLoadPipelineFile}
              />
              <ArtifactsFileField
                key={artifacts ? 'detector-cargado' : 'detector-vacio'}
                accent="violet"
                fileName={artifacts?.name}
                onChange={(event) => selectArtifacts(event.target.files[0] ?? null)}
              />
              <SchemaBuilderField accent="violet" fields={schemaFields} onChange={changeSchemaFields} />
            </GradientCard>
          </div>
        </div>
      </div>
    </form>
  )
}
