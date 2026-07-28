export function ChartCard({ title, icon, children }) {
  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-emerald-200/60 shadow-sm p-5 flex flex-col gap-3">
      <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2">
        {icon && <span className="text-emerald-500">{icon}</span>}
        {title}
      </h4>
      {children}
    </div>
  )
}
