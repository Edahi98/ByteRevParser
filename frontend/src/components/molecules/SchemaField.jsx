import { Label } from '../atoms/Label'
import { TextArea } from '../atoms/TextArea'

export function SchemaField({ value, onChange, accent = 'indigo' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="pipeline-schema">Esquema de extracción (JSON)</Label>
      <p className="text-xs text-slate-500 mb-1">
        Escribe la plantilla JSON con la estructura y nombres de campo que esperas.
      </p>
      <TextArea id="pipeline-schema" value={value} onChange={onChange} rows={5} accent={accent} />
    </div>
  )
}


