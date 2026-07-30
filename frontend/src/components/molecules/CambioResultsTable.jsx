export function CambioResultsTable({ resultados }) {
  return (
    <div className="w-full overflow-auto max-h-72 rounded-2xl border border-teal-200/60 bg-white/90 backdrop-blur-sm shadow-sm">
      <table className="w-full text-sm">
        <thead className="bg-teal-50/80 sticky top-0">
          <tr>
            <th className="text-left font-bold text-teal-800 px-4 py-2.5">Frase</th>
            <th className="text-left font-bold text-teal-800 px-4 py-2.5">¿La conoce?</th>
            <th className="text-left font-bold text-teal-800 px-4 py-2.5">Se parece más a</th>
          </tr>
        </thead>
        <tbody>
          {resultados.map((resultado, index) => (
            <tr key={`${resultado.frase}-${index}`} className="border-t border-teal-100/80">
              <td className="px-4 py-2 text-slate-700">{resultado.frase}</td>
              <td className="px-4 py-2">
                <span
                  className={
                    resultado.es_conocida
                      ? 'inline-block bg-gradient-to-r from-emerald-100 to-teal-100 text-teal-800 text-xs font-semibold px-2.5 py-1 rounded-full border border-teal-200/70'
                      : 'inline-block bg-slate-100 text-slate-600 text-xs font-semibold px-2.5 py-1 rounded-full border border-slate-200'
                  }
                >
                  {resultado.es_conocida ? 'Sí, la conoce' : 'Es nueva'}
                </span>
              </td>
              <td className="px-4 py-2 text-slate-500 text-xs">{resultado.frase_mas_parecida}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
