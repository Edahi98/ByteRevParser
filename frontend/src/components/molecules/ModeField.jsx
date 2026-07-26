import { Label } from '../atoms/Label'
import { Select } from '../atoms/Select'
import { pipelineModes } from '../../data/pipelineModes'

export function ModeField({ value, onChange, options = pipelineModes, disabled = false, accent = 'indigo' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="pipeline-mode">¿Cómo quieres el resultado?</Label>
      <Select id="pipeline-mode" value={value} onChange={onChange} options={options} disabled={disabled} accent={accent} />
      {disabled ? (
        <p className="text-xs text-amber-600 font-medium">
          El modo de salida no aplica cuando se usa un esquema personalizado.
        </p>
      ) : (
        <p className="text-xs text-slate-500">
          Elige el formato estructural de la salida procesada.
        </p>
      )}
    </div>
  )
}


