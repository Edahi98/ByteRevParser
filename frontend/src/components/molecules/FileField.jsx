import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'

const ACCEPTED_EXTENSIONS = '.doc,.docx,.xls,.xlsx,.pdf'

export function FileField({ fileName, onChange, accent = 'blue' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="pipeline-file">Documento (PDF, Word, Excel)</Label>
      <FileInput id="pipeline-file" accept={ACCEPTED_EXTENSIONS} onChange={onChange} accent={accent} />
      <p className="text-xs text-slate-500">Formatos soportados: .doc, .docx, .xls, .xlsx, .pdf</p>
      {fileName && (
        <div className="mt-1 inline-flex items-center gap-2 bg-blue-50 border border-blue-200/80 text-blue-800 text-xs font-medium px-3 py-1.5 rounded-md w-fit">
          <span>📄</span>
          <span>Seleccionado: <strong className="font-semibold">{fileName}</strong></span>
        </div>
      )}
    </div>
  )
}


