import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function ModelNameField({ value, onChange, accent = 'emerald' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="model-name">¿Cómo quieres llamar a este modelo?</Label>
      <TextInput
        id="model-name"
        value={value}
        onChange={onChange}
        placeholder="ej. clasificador_soporte"
        accent={accent}
      />
      <p className="text-xs text-slate-500">
        Te sirve para reconocerlo después, sobre todo si vas a entrenar y usar varios modelos a la vez.
      </p>
    </div>
  )
}
