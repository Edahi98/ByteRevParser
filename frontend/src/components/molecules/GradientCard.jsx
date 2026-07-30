const GRADIENT_CLASSES = {
  emerald: 'from-emerald-400 to-teal-500',
  sky: 'from-sky-400 to-blue-500',
  violet: 'from-violet-400 to-fuchsia-500',
  amber: 'from-amber-400 to-orange-500',
  blue: 'from-blue-400 to-indigo-500',
}

export function GradientCard({ icon, title, gradient = 'emerald', children }) {
  const gradientClass = GRADIENT_CLASSES[gradient] || GRADIENT_CLASSES.emerald

  return (
    <div className="rounded-3xl bg-white shadow-lg shadow-slate-200/60 border border-slate-100 overflow-hidden flex flex-col">
      <div className={`bg-gradient-to-r ${gradientClass} px-6 py-5 flex items-center gap-3`}>
        <div className="w-11 h-11 shrink-0 rounded-2xl bg-white/25 backdrop-blur flex items-center justify-center text-white text-xl shadow-inner">
          {icon}
        </div>
        <h2 className="text-lg font-bold text-white tracking-tight">{title}</h2>
      </div>
      <div className="p-6 flex flex-col gap-4">{children}</div>
    </div>
  )
}
