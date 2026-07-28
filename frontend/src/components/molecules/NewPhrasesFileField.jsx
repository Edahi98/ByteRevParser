import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTable } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'

export function NewPhrasesFileField({ fileName, onChange, accent = 'teal' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="new-phrases-file">Frases que quieres clasificar (archivo CSV)</Label>
      <FileInput id="new-phrases-file" accept=".csv" onChange={onChange} accent={accent} />
      <p className="text-xs text-slate-500">Debe tener una columna "frase" con una frase por fila.</p>
      {fileName && (
        <div className="mt-1 inline-flex items-center gap-2 bg-teal-50 border border-teal-200/80 text-teal-800 text-xs font-medium px-3 py-1.5 rounded-md w-fit">
          <span><FontAwesomeIcon icon={faTable} /></span>
          <span>Archivo seleccionado: <strong className="font-semibold">{fileName}</strong></span>
        </div>
      )}
    </div>
  )
}
