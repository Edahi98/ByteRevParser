export function ClusterSummaryTable({ clusters }) {
  return (
    <div className="w-full overflow-auto rounded-2xl border border-emerald-200/60 bg-white/90 backdrop-blur-sm shadow-sm">
      <table className="w-full text-sm">
        <thead className="bg-emerald-50/80">
          <tr>
            <th className="text-left font-bold text-emerald-800 px-4 py-2.5">Grupo</th>
            <th className="text-right font-bold text-emerald-800 px-4 py-2.5">Frases</th>
            <th className="text-left font-bold text-emerald-800 px-4 py-2.5">Fragmentos característicos</th>
            <th className="text-left font-bold text-emerald-800 px-4 py-2.5">Ejemplos</th>
          </tr>
        </thead>
        <tbody>
          {clusters.map((cluster) => (
            <tr key={cluster.cluster_id} className="border-t border-emerald-100/80">
              <td className="px-4 py-2 font-semibold text-slate-700 align-top">Grupo {cluster.cluster_id}</td>
              <td className="px-4 py-2 text-right text-slate-600 align-top">{cluster.tamano}</td>
              <td className="px-4 py-2 text-slate-600 align-top">
                <div className="flex flex-wrap gap-1.5">
                  {cluster.terminos_clave.map((termino) => (
                    <span
                      key={termino}
                      className="inline-block bg-emerald-50 text-emerald-700 text-xs font-medium px-2 py-0.5 rounded-full border border-emerald-200/70"
                    >
                      {termino}
                    </span>
                  ))}
                </div>
              </td>
              <td className="px-4 py-2 text-slate-500 text-xs align-top">
                <ul className="flex flex-col gap-1 list-disc list-inside">
                  {cluster.ejemplos.map((ejemplo, index) => (
                    <li key={index}>{ejemplo}</li>
                  ))}
                </ul>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
