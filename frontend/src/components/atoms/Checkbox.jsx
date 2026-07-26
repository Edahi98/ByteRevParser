const ACCENT_CLASSES = {
  blue: 'border-slate-300 text-blue-600 focus:ring-2 focus:ring-blue-500/30 accent-blue-600',
  sky: 'border-slate-300 text-sky-600 focus:ring-2 focus:ring-sky-500/30 accent-sky-600',
  cyan: 'border-slate-300 text-cyan-600 focus:ring-2 focus:ring-cyan-500/30 accent-cyan-600',
  indigo: 'border-slate-300 text-indigo-600 focus:ring-2 focus:ring-indigo-500/30 accent-indigo-600',
  purple: 'border-slate-300 text-purple-600 focus:ring-2 focus:ring-purple-500/30 accent-purple-600',
  teal: 'border-slate-300 text-teal-600 focus:ring-2 focus:ring-teal-500/30 accent-teal-600',
}

export function Checkbox({ id, checked, onChange, disabled = false, accent = 'blue' }) {
  const accentStyle = ACCENT_CLASSES[accent] || ACCENT_CLASSES.blue

  return (
    <input
      id={id}
      type="checkbox"
      checked={checked}
      onChange={onChange}
      disabled={disabled}
      className={`h-4 w-4 rounded border cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 transition-colors ${accentStyle}`}
    />
  )
}


