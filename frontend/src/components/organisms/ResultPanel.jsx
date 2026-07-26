export function ResultPanel({ result, error, isLoading }) {
  if (isLoading) {
    return (
      <section className="w-full py-12 bg-blue-50/50 border-t border-blue-100">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex items-center justify-center gap-3 text-blue-700">
          <svg className="animate-spin h-5 w-5 text-blue-600" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span className="font-semibold text-sm">Procesando información en el servidor...</span>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="w-full py-12 bg-red-50/60 border-t border-red-200/80">
        <div className="max-w-4xl mx-auto px-4 md:px-6 flex items-start gap-3 text-red-700">
          <span className="text-xl leading-none">⚠️</span>
          <div className="flex-1">
            <h4 className="font-bold text-sm text-red-800 mb-0.5">Error en la ejecución</h4>
            <p className="text-xs text-red-700">{error}</p>
          </div>
        </div>
      </section>
    )
  }

  if (!result) return null

  return (
    <section className="w-full py-12 md:py-16 bg-slate-50 border-t border-slate-200/80">
      <div className="max-w-4xl mx-auto px-4 md:px-6 flex flex-col gap-4">
        <div className="flex flex-wrap items-center justify-between border-b border-slate-200/80 pb-4 gap-2">
          <h3 className="text-base font-bold text-slate-800 tracking-tight flex items-center gap-2.5">
            <span className="w-7 h-7 rounded-lg bg-emerald-100/80 text-emerald-700 border border-emerald-200 flex items-center justify-center text-xs font-bold">
              ✓
            </span>
            Resultado del procesamiento
          </h3>
          <div className="flex items-center gap-2 text-xs">
            <span className="bg-white text-slate-700 font-medium px-3 py-1 rounded-md border border-slate-200 shadow-2xs">
              📄 {result.filename}
            </span>
            <span className="bg-blue-100/80 text-blue-800 font-medium px-3 py-1 rounded-md border border-blue-200">
              {result.mode}
            </span>
          </div>
        </div>
        <pre className="w-full overflow-auto max-h-96 font-mono text-xs bg-slate-900 text-slate-100 rounded-lg p-5 leading-relaxed shadow-inner">
          {typeof result.result === 'string' ? result.result : JSON.stringify(result.result, null, 2)}
        </pre>
      </div>
    </section>
  )
}


