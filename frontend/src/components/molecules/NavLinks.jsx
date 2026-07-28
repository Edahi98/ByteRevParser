import { NavLink } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileLines, faBrain } from '@fortawesome/free-solid-svg-icons'

const LINK_BASE = 'inline-flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors'
const LINK_ACTIVE = 'bg-white/20 text-white'
const LINK_INACTIVE = 'text-white/80 hover:text-white hover:bg-white/10'

export function NavLinks() {
  return (
    <nav className="flex items-center gap-1.5">
      <NavLink to="/" end className={({ isActive }) => `${LINK_BASE} ${isActive ? LINK_ACTIVE : LINK_INACTIVE}`}>
        <FontAwesomeIcon icon={faFileLines} /> Extractor
      </NavLink>
      <NavLink
        to="/clasificador-texto"
        className={({ isActive }) => `${LINK_BASE} ${isActive ? LINK_ACTIVE : LINK_INACTIVE}`}
      >
        <FontAwesomeIcon icon={faBrain} /> Clasificador de texto
      </NavLink>
    </nav>
  )
}
