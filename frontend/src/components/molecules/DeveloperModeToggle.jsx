import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGear } from '@fortawesome/free-solid-svg-icons'

export function DeveloperModeToggle({ isOpen, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className="inline-flex items-center gap-2 text-xs font-medium text-slate-500 hover:text-indigo-600 transition-colors py-1 cursor-pointer group"
    >
      <span className="text-sm transition-transform duration-200 group-hover:rotate-45">
        <FontAwesomeIcon icon={faGear} />
      </span>
      <span>{isOpen ? 'Ocultar Modo Desarrollador' : 'Modo Desarrollador'}</span>
      <span className="text-[10px] text-slate-400 font-normal">
        {isOpen ? '▲' : '▼ (Pipeline JSON, Formato de salida, Búsqueda)'}
      </span>
    </button>
  )
}

