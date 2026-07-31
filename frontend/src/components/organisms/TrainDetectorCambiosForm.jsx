import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBolt } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'

function formatearTiempo(segundos) {
  const minutos = Math.floor(segundos / 60)
  const segundosRestantes = segundos % 60
  return `${minutos}:${String(segundosRestantes).padStart(2, '0')}`
}

export function TrainDetectorCambiosForm({ onSubmit, isLoading, progress, error }) {
  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit()
  }

  return (
    <form onSubmit={handleSubmit}>
      <GradientCard icon={<FontAwesomeIcon icon={faBolt} />} title="Detector de cambios" gradient="emerald">
        <Button type="submit" variant="green" disabled={isLoading}>
          {isLoading ? (
            <span className="inline-flex items-center justify-center gap-2">
              <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Creando detector...
            </span>
          ) : (
            'Crear detector'
          )}
        </Button>

        {isLoading && progress && (
          <div className="flex flex-col gap-1.5">
            <div className="w-full h-2 bg-emerald-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all"
                style={{
                  width: `${progress.epocas_totales ? Math.round((progress.epoca_actual / progress.epocas_totales) * 100) : 0}%`,
                }}
              />
            </div>
            <span className="text-xs text-slate-500">
              Vuelta {progress.epoca_actual} de {progress.epocas_totales} · {formatearTiempo(progress.segundos_transcurridos)} transcurridos
            </span>
          </div>
        )}

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}
      </GradientCard>
    </form>
  )
}
