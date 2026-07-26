import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function QueryField({ value, onChange, accent = 'cyan' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="pipeline-query">¿Qué estás buscando? (opcional)</Label>
      <TextInput
        id="pipeline-query"
        value={value}
        onChange={onChange}
        placeholder="ej. ingresos por producto, resumen de ventas..."
        accent={accent}
      />
      <p className="text-xs text-slate-500">
        Escribe palabras o conceptos clave para filtrar y ordenar los fragmentos más relevantes.
      </p>
    </div>
  )
}


