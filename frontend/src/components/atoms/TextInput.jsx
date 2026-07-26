const ACCENT_CLASSES = {
  blue: 'focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600 border-slate-300',
  sky: 'focus:ring-2 focus:ring-sky-500/20 focus:border-sky-600 border-slate-300',
  cyan: 'focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-600 border-slate-300',
  indigo: 'focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 border-slate-300',
  purple: 'focus:ring-2 focus:ring-purple-500/20 focus:border-purple-600 border-slate-300',
  teal: 'focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 border-slate-300',
}

export function TextInput({ id, type = 'text', value, onChange, placeholder, min, disabled = false, accent = 'blue' }) {
  const accentStyle = ACCENT_CLASSES[accent] || ACCENT_CLASSES.blue

  return (
    <input
      id={id}
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      min={min}
      disabled={disabled}
      className={`w-full px-3.5 py-2 text-sm text-slate-800 bg-white border rounded-lg shadow-2xs focus:outline-none transition-all placeholder:text-slate-400 disabled:bg-slate-100 disabled:text-slate-400 disabled:cursor-not-allowed ${accentStyle}`}
    />
  )
}


