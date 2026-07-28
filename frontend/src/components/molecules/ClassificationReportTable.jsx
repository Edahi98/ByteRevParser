const EXCLUDED_ROWS = new Set(['accuracy'])

export function ClassificationReportTable({ classificationReport }) {
  const rows = Object.entries(classificationReport).filter(([key]) => !EXCLUDED_ROWS.has(key))

  return (
    <div className="w-full overflow-auto rounded-2xl border border-emerald-200/60 bg-white/90 backdrop-blur-sm shadow-sm">
      <table className="w-full text-sm">
        <thead className="bg-emerald-50/80">
          <tr>
            <th className="text-left font-bold text-emerald-800 px-4 py-2.5">Clase</th>
            <th className="text-right font-bold text-emerald-800 px-4 py-2.5">Precisión</th>
            <th className="text-right font-bold text-emerald-800 px-4 py-2.5">Recall</th>
            <th className="text-right font-bold text-emerald-800 px-4 py-2.5">F1-score</th>
            <th className="text-right font-bold text-emerald-800 px-4 py-2.5">Soporte</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([label, metrics]) => (
            <tr key={label} className="border-t border-emerald-100/80">
              <td className="px-4 py-2 font-semibold text-slate-700">{label}</td>
              <td className="px-4 py-2 text-right text-slate-600">{metrics.precision.toFixed(2)}</td>
              <td className="px-4 py-2 text-right text-slate-600">{metrics.recall.toFixed(2)}</td>
              <td className="px-4 py-2 text-right text-slate-600">{metrics['f1-score'].toFixed(2)}</td>
              <td className="px-4 py-2 text-right text-slate-600">{metrics.support}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
