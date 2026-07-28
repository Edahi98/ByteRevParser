import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function PhraseField({ value, onChange, accent = 'teal' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="classify-phrase">¿Qué frase quieres clasificar?</Label>
      <TextInput
        id="classify-phrase"
        value={value}
        onChange={onChange}
        placeholder="ej. no puedo iniciar sesión en mi cuenta"
        accent={accent}
      />
    </div>
  )
}
