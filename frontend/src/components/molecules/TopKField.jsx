import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function TopKField({ value, onChange, disabled, accent = 'cyan' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="pipeline-top-k">¿Cuántos resultados quieres? (opcional)</Label>
      <TextInput
        id="pipeline-top-k"
        type="number"
        min={1}
        value={value}
        onChange={onChange}
        placeholder="Todos los resultados"
        disabled={disabled}
        accent={accent}
      />
      <p className="text-xs text-slate-500">
        Límite máximo de fragmentos más relevantes a obtener (deja vacío para obtener todos).
      </p>
    </div>
  )
}


