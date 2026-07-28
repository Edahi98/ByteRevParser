import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTable } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'

export function DatasetFileField({ fileName, onChange, accent = 'emerald' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="dataset-file">Tus ejemplos ya clasificados (archivo CSV)</Label>
      <FileInput id="dataset-file" accept=".csv" onChange={onChange} accent={accent} />
      <p className="text-xs text-slate-500">
        Debe tener una columna "frase" y una columna "etiqueta". Tus propias etiquetas se convierten automáticamente en las clases del modelo.
      </p>
      {fileName && (
        <div className="mt-1 inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-medium px-3 py-1.5 rounded-md w-fit">
          <span><FontAwesomeIcon icon={faTable} /></span>
          <span>Archivo seleccionado: <strong className="font-semibold">{fileName}</strong></span>
        </div>
      )}
    </div>
  )
}
