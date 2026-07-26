const ACCENT_ICON_CLASSES = {
  blue: 'bg-blue-100/80 text-blue-700 border-blue-200/70',
  sky: 'bg-sky-100/80 text-sky-700 border-sky-200/70',
  cyan: 'bg-cyan-100/80 text-cyan-700 border-cyan-200/70',
  indigo: 'bg-indigo-100/80 text-indigo-700 border-indigo-200/70',
  purple: 'bg-purple-100/80 text-purple-700 border-purple-200/70',
  teal: 'bg-teal-100/80 text-teal-700 border-teal-200/70',
}

export function SectionTitle({ children, icon, accent = 'blue' }) {
  const iconStyle = ACCENT_ICON_CLASSES[accent] || ACCENT_ICON_CLASSES.blue

  return (
    <h2 className="text-base md:text-lg font-bold text-slate-800 tracking-tight flex items-center gap-3">
      {icon && (
        <span className={`w-8 h-8 rounded-lg border flex items-center justify-center text-base select-none ${iconStyle}`}>
          {icon}
        </span>
      )}
      <span>{children}</span>
    </h2>
  )
}


