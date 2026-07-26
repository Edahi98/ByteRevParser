import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLightbulb, faCheck, faPlus, faXmark } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'
import { Button } from '../atoms/Button'

const QUICK_SUGGESTIONS = [
  'Versión',
  'Fecha de revisión',
  'Descripción del cambio',
  'Elaboró',
  'Revisó',
  'Aprobó',
  'Realizó',
]

export function SchemaBuilderField({ fields = [''], onChange, accent = 'blue' }) {
  const handleFieldChange = (index, newValue) => {
    const updated = [...fields]
    updated[index] = newValue
    onChange(updated)
  }

  const handleAddField = () => {
    onChange([...fields, ''])
  }

  const handleRemoveField = (index) => {
    const updated = fields.filter((_, i) => i !== index)
    onChange(updated.length > 0 ? updated : [''])
  }

  const handleAddSuggestion = (suggestion) => {
    if (fields.includes(suggestion)) return

    const emptyIndex = fields.findIndex((f) => f.trim() === '')
    if (emptyIndex !== -1) {
      const updated = [...fields]
      updated[emptyIndex] = suggestion
      onChange(updated)
    } else {
      onChange([...fields, suggestion])
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <Label htmlFor="schema-field-0">¿Qué datos del control de cambios quieres obtener?</Label>
        <p className="text-xs text-slate-500 mt-1">
          Escribe los campos del control de cambios que quieres extraer (ej. versión, fecha de revisión, quién lo elaboró) o selecciona alguna de las sugerencias rápidas.
        </p>
      </div>

      <div className="flex flex-col gap-2 bg-slate-50/80 p-3.5 rounded-xl border border-slate-200/60">
        <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
          <FontAwesomeIcon icon={faLightbulb} className="text-amber-500" /> Sugerencias rápidas:
        </span>
        <div className="flex flex-wrap gap-2">
          {QUICK_SUGGESTIONS.map((suggestion) => {
            const isSelected = fields.includes(suggestion)
            return (
              <div key={suggestion} className="shrink-0">
                <Button
                  variant="secondary"
                  onClick={() => handleAddSuggestion(suggestion)}
                  disabled={isSelected}
                >
                  <span className="text-xs flex items-center gap-1.5">
                    <FontAwesomeIcon icon={isSelected ? faCheck : faPlus} /> {suggestion}
                  </span>
                </Button>
              </div>
            )
          })}
        </div>
      </div>

      <div className="flex flex-col gap-2.5">
        {fields.map((field, index) => (
          <div key={index} className="flex items-center gap-2 transition-all">
            <div className="flex-1">
              <TextInput
                id={`schema-field-${index}`}
                value={field}
                onChange={(e) => handleFieldChange(index, e.target.value)}
                placeholder={`Ej. ${QUICK_SUGGESTIONS[index % QUICK_SUGGESTIONS.length]}`}
                accent={accent}
              />
            </div>
            <div className="shrink-0">
              <Button
                variant="secondary"
                onClick={() => handleRemoveField(index)}
                disabled={fields.length === 1 && field === ''}
              >
                <FontAwesomeIcon icon={faXmark} />
              </Button>
            </div>
          </div>
        ))}
      </div>

      <div className="pt-1">
        <Button variant="secondary" onClick={handleAddField}>
          <span className="inline-flex items-center gap-1.5">
            <FontAwesomeIcon icon={faPlus} /> Agregar otro campo
          </span>
        </Button>
      </div>
    </div>
  )
}

