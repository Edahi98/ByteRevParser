import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function TopKField({ value, onChange, disabled, accent = 'blue' }) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="pipeline-top-k">¿Cuántos resultados? (opcional)</Label>
      <TextInput
        id="pipeline-top-k"
        type="number"
        min={1}
        value={value}
        onChange={onChange}
        placeholder="Todos"
        disabled={disabled}
        accent={accent}
      />
    </div>
  )
}
