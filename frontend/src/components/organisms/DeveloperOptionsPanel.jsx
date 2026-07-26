import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faScrewdriverWrench, faBolt, faMagnifyingGlass, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons'
import { FormSection } from '../molecules/FormSection'
import { PipelineJsonField } from '../molecules/PipelineJsonField'
import { SchemaToggleField } from '../molecules/SchemaToggleField'
import { ModeField } from '../molecules/ModeField'
import { SchemaField } from '../molecules/SchemaField'
import { QueryField } from '../molecules/QueryField'
import { TopKField } from '../molecules/TopKField'
import { pipelineModes } from '../../data/pipelineModes'

export function DeveloperOptionsPanel({
  pipeline,
  onPipelineChange,
  onLoadPipelineFile,
  mode,
  onModeChange,
  useSchema,
  onUseSchemaChange,
  schema,
  onSchemaChange,
  query,
  onQueryChange,
  topK,
  onTopKChange,
}) {
  return (
    <div className="w-full border-t-2 border-indigo-200 bg-indigo-50/40">
      <div className="w-full py-4">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex items-center gap-3">
          <span className="w-9 h-9 shrink-0 rounded-lg bg-indigo-100 text-indigo-600 border border-indigo-200 flex items-center justify-center">
            <FontAwesomeIcon icon={faWandMagicSparkles} />
          </span>
          <div>
            <p className="text-sm font-bold text-indigo-900">Opciones avanzadas</p>
            <p className="text-xs text-indigo-700/80">
              Ajusta a detalle cómo se extrae el control de cambios: el pipeline técnico, el formato de salida y la búsqueda avanzada.
            </p>
          </div>
        </div>
      </div>

      <FormSection
        title="Pipeline JSON"
        icon={<FontAwesomeIcon icon={faScrewdriverWrench} />}
        accent="indigo"
        subtitle="Modifica la definición del pipeline o carga un archivo JSON personalizado"
      >
        <PipelineJsonField accent="indigo" value={pipeline} onChange={onPipelineChange} onLoadFile={onLoadPipelineFile} />
      </FormSection>

      <FormSection
        title="Formato y Esquema Avanzado"
        icon={<FontAwesomeIcon icon={faBolt} />}
        accent="indigo"
        subtitle="Desactiva el esquema para usar el modo clásico (Texto / XML) o define un esquema JSON avanzado — por ejemplo, para extraer una tabla de control de cambios completa"
      >
        <SchemaToggleField accent="indigo" checked={useSchema} onChange={onUseSchemaChange} />
        <ModeField accent="indigo" value={mode} onChange={onModeChange} options={pipelineModes} disabled={useSchema} />
        {useSchema && <SchemaField accent="indigo" value={schema} onChange={onSchemaChange} />}
      </FormSection>

      <FormSection
        title="Búsqueda por Relevancia"
        icon={<FontAwesomeIcon icon={faMagnifyingGlass} />}
        accent="cyan"
        subtitle="Filtra y ordena la información por palabras clave (query / top_k)"
      >
        <QueryField accent="cyan" value={query} onChange={onQueryChange} />
        <TopKField accent="cyan" value={topK} onChange={onTopKChange} disabled={!query} />
      </FormSection>
    </div>
  )
}
