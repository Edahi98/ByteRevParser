import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faKey } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

export function QueryField({ value, onChange, accent = 'blue' }) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="pipeline-query">
        <FontAwesomeIcon icon={faKey} className="mr-1.5 text-blue-500" />
        Palabra clave (opcional)
      </Label>
      <TextInput
        id="pipeline-query"
        value={value}
        onChange={onChange}
        placeholder="ej. ingresos por producto"
        accent={accent}
      />
    </div>
  )
}
