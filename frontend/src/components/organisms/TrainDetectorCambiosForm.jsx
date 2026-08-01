import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBolt } from '@fortawesome/free-solid-svg-icons'
import { Button } from '../atoms/Button'
import { GradientCard } from '../molecules/GradientCard'

export function TrainDetectorCambiosForm({ onSubmit, isLoading, error }) {
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

        {error && (
          <p className="text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-fit">
            {error}
          </p>
        )}
      </GradientCard>
    </form>
  )
}
