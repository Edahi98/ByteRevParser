import { NavLinks } from '../molecules/NavLinks'

const ACCENT_CLASSES = {
  blue: 'bg-blue-600 border-blue-700',
  green: 'bg-gradient-to-r from-emerald-600 to-teal-600 border-teal-700/60',
}

const BADGE_CLASSES = {
  blue: 'bg-blue-800/80 text-blue-100 border-blue-400/30',
  green: 'bg-black/15 text-white border-white/25',
}

export function Header({ title, subtitle, accent = 'blue' }) {
  const headerStyle = ACCENT_CLASSES[accent] || ACCENT_CLASSES.blue
  const badgeStyle = BADGE_CLASSES[accent] || BADGE_CLASSES.blue

  return (
    <header className={`w-full border-b text-white shadow-sm ${headerStyle}`}>
      <div className="w-full max-w-4xl mx-auto px-4 md:px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-white/15 border border-white/25 flex items-center justify-center font-black text-xl tracking-tighter text-white shadow-inner select-none">
            DR
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-white tracking-tight leading-none">{title}</h1>
              <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded border ${badgeStyle}`}>
                OLAN Platform
              </span>
            </div>
            {subtitle && (
              <p className="text-xs text-white/90 mt-0.5 font-normal leading-snug">
                {subtitle}
              </p>
            )}
          </div>
        </div>

        <NavLinks />
      </div>
    </header>
  )
}
