import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFolderOpen } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { TextArea } from '../atoms/TextArea'

export function PipelineJsonField({ value, onChange, onLoadFile, accent = 'blue' }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center justify-between mb-0.5">
        <Label htmlFor="pipeline-json">JSON del pipeline</Label>
        <label
          htmlFor="pipeline-json-file"
          className="text-xs font-semibold text-blue-600 hover:text-blue-800 cursor-pointer inline-flex items-center gap-1 hover:underline transition-all"
        >
          <span><FontAwesomeIcon icon={faFolderOpen} /></span> Cargar desde archivo
        </label>
      </div>
      <p className="text-xs text-slate-500 mb-1">
        Configuración técnica del proceso (no la edites si no sabes qué hace)
      </p>
      <input
        id="pipeline-json-file"
        type="file"
        accept=".json,application/json"
        onChange={onLoadFile}
        className="hidden"
      />
      <TextArea id="pipeline-json" value={value} onChange={onChange} accent={accent} />
    </div>
  )
}



