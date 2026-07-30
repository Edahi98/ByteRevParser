import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFolderOpen, faCheck } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'

export function PipelineJsonField({ fileName, onLoadFile }) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="pipeline-json-file">Configuración</Label>
      <label
        htmlFor="pipeline-json-file"
        className="inline-flex items-center justify-center gap-2 w-full sm:w-fit bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg py-2 px-4 transition-all text-sm border border-slate-200 cursor-pointer shadow-sm"
      >
        <FontAwesomeIcon icon={faFolderOpen} className="text-violet-500" /> Cargar archivo
      </label>
      <input
        id="pipeline-json-file"
        type="file"
        accept=".json,application/json"
        onChange={onLoadFile}
        className="hidden"
      />
      {fileName && (
        <span className="text-xs text-blue-700 font-medium inline-flex items-center gap-1.5">
          <FontAwesomeIcon icon={faCheck} /> {fileName}
        </span>
      )}
    </div>
  )
}
