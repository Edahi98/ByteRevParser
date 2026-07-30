import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTriangleExclamation, faCheck, faFileLines } from '@fortawesome/free-solid-svg-icons'

export function ResultPanel({ result, error, isLoading }) {
  if (isLoading) {
    return (
      <section className="w-full py-12 bg-gradient-to-b from-blue-50/60 to-white">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex items-center justify-center gap-3 text-blue-700">
          <svg className="animate-spin h-5 w-5 text-blue-600" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span className="font-semibold text-sm">Buscando...</span>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="w-full py-10">
        <div className="max-w-4xl mx-auto px-4 md:px-6">
          <div className="rounded-3xl bg-gradient-to-r from-red-400 to-rose-500 p-0.5 shadow-lg shadow-red-200/60">
            <div className="rounded-[22px] bg-white px-6 py-5 flex items-start gap-3">
              <span className="w-10 h-10 shrink-0 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center text-lg">
                <FontAwesomeIcon icon={faTriangleExclamation} />
              </span>
              <div className="flex-1">
                <h4 className="font-bold text-sm text-red-800 mb-0.5">No se pudo extraer</h4>
                <p className="text-xs text-red-700">{error}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    )
  }

  if (!result) return null

  return (
    <section className="w-full py-10 md:py-14">
      <div className="max-w-4xl mx-auto px-4 md:px-6">
        <div className="rounded-3xl bg-white shadow-lg shadow-slate-200/60 border border-slate-100 overflow-hidden">
          <div className="bg-gradient-to-r from-emerald-400 to-teal-500 px-6 py-5 flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-3">
              <span className="w-11 h-11 shrink-0 rounded-2xl bg-white/25 backdrop-blur flex items-center justify-center text-xl">
                <FontAwesomeIcon icon={faCheck} />
              </span>
              Listo
            </h3>
            <span className="bg-white/20 text-white font-medium px-3 py-1 rounded-full text-xs inline-flex items-center gap-1.5">
              <FontAwesomeIcon icon={faFileLines} /> {result.filename}
            </span>
          </div>
          <div className="p-6">
            <pre className="w-full overflow-auto max-h-96 font-mono text-xs bg-slate-900 text-slate-100 rounded-2xl p-5 leading-relaxed shadow-inner">
              {typeof result.result === 'string' ? result.result : JSON.stringify(result.result, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </section>
  )
}
