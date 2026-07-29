import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSliders } from '@fortawesome/free-solid-svg-icons'

export function UsedConfigSummary({ configuracion }) {
  const items = [
    { etiqueta: 'Fragmentos de letras', valor: `${configuracion.tfidf.ngram_range[0]} a ${configuracion.tfidf.ngram_range[1]} caracteres` },
    { etiqueta: 'Vocabulario máximo', valor: configuracion.tfidf.max_features.toLocaleString('es-MX') },
    { etiqueta: 'Nivel de detalle interno', valor: configuracion.autoencoder.bottleneck_dim },
    { etiqueta: 'Repasos de entrenamiento', valor: configuracion.autoencoder.epochs },
    { etiqueta: 'Grupos probados', valor: `${configuracion.clustering.k_min} a ${configuracion.clustering.k_max}` },
    { etiqueta: 'Ruido esperado', valor: `${Math.round(configuracion.novelty.contamination * 100)}%` },
  ]

  return (
    <div className="flex flex-col gap-2">
      <p className="text-xs font-semibold text-emerald-800 inline-flex items-center gap-1.5">
        <FontAwesomeIcon icon={faSliders} /> Con qué ajustes se entrenó este modelo
      </p>
      <div className="flex flex-wrap gap-2">
        {items.map((item) => (
          <span
            key={item.etiqueta}
            className="inline-flex items-center gap-1.5 bg-white border border-emerald-200/70 rounded-full px-3 py-1.5 text-xs"
          >
            <span className="text-slate-500">{item.etiqueta}:</span>
            <span className="font-semibold text-emerald-700">{item.valor}</span>
          </span>
        ))}
      </div>
    </div>
  )
}
