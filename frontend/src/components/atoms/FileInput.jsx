const ACCENT_CLASSES = {
  blue: 'file:bg-blue-600 hover:file:bg-blue-700 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600 border-slate-300',
  sky: 'file:bg-sky-600 hover:file:bg-sky-700 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-600 border-slate-300',
  cyan: 'file:bg-cyan-600 hover:file:bg-cyan-700 focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-600 border-slate-300',
  indigo: 'file:bg-indigo-600 hover:file:bg-indigo-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 border-slate-300',
  purple: 'file:bg-purple-600 hover:file:bg-purple-700 focus:ring-2 focus:ring-purple-500/20 focus:border-purple-600 border-slate-300',
  teal: 'file:bg-teal-600 hover:file:bg-teal-700 focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 border-slate-300',
  emerald: 'file:bg-emerald-600 hover:file:bg-emerald-700 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-600 border-slate-300',
  violet: 'file:bg-violet-600 hover:file:bg-violet-700 focus:ring-2 focus:ring-violet-500/20 focus:border-violet-600 border-slate-300',
  amber: 'file:bg-amber-600 hover:file:bg-amber-700 focus:ring-2 focus:ring-amber-500/20 focus:border-amber-600 border-slate-300',
}

export function FileInput({ id, accept, onChange, accent = 'blue' }) {
  const accentStyle = ACCENT_CLASSES[accent] || ACCENT_CLASSES.blue

  return (
    <input
      id={id}
      type="file"
      accept={accept}
      onChange={onChange}
      className={`w-full text-sm text-slate-700 file:mr-3 file:px-3.5 file:py-1.5 file:rounded-md file:border-0 file:text-xs file:font-semibold file:text-white border rounded-lg bg-slate-50/50 hover:bg-white p-2 transition-all cursor-pointer focus:outline-none ${accentStyle}`}
    />
  )
}


