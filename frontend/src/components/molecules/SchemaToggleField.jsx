import { Checkbox } from '../atoms/Checkbox'

export function SchemaToggleField({ checked, onChange, accent = 'indigo' }) {
  return (
    <div className="flex flex-col gap-1 pt-1">
      <div className="flex items-center gap-2.5">
        <Checkbox id="pipeline-use-schema" checked={checked} onChange={onChange} accent={accent} />
        <label
          htmlFor="pipeline-use-schema"
          className="text-sm font-semibold text-slate-800 cursor-pointer select-none"
        >
          Quiero que me devuelva datos en un formato específico (avanzado)
        </label>
      </div>
      <p className="text-xs text-slate-500 pl-6.5">
        Usa NuExtract para definir exactamente los campos JSON requeridos.
      </p>
    </div>
  )
}


