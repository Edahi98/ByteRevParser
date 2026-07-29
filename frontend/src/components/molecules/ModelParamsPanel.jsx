import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSliders } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { RangeSlider } from '../atoms/RangeSlider'

export function ModelParamsPanel({ params, onChange, accent = 'emerald' }) {
  const [isOpen, setIsOpen] = useState(false)

  const setParam = (key) => (event) => {
    onChange({ ...params, [key]: Number(event.target.value) })
  }

  return (
    <div className="flex flex-col gap-3">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="inline-flex items-center gap-2 text-xs font-medium text-slate-500 hover:text-emerald-600 transition-colors py-1 cursor-pointer group w-fit"
      >
        <span className="text-sm transition-transform duration-200 group-hover:rotate-12">
          <FontAwesomeIcon icon={faSliders} />
        </span>
        <span>{isOpen ? 'Ocultar ajustes del modelo' : 'Ajustar cómo aprende el modelo (opcional)'}</span>
        <span className="text-[10px] text-slate-400 font-normal">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="flex flex-col gap-6 bg-emerald-50/50 border border-emerald-200/70 rounded-xl px-4 py-4">
          <p className="text-xs text-slate-500 -mb-1">
            Si no sabes qué significan, déjalos como están: los valores actuales funcionan bien para la mayoría de los casos.
          </p>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-ngram-min">
              Tamaño de los pedacitos de letras: de {params.ngramMin} a {params.ngramMax} caracteres
            </Label>
            <p className="text-xs text-slate-500">
              En vez de comparar palabras completas, el modelo compara pedacitos cortos de letras — así reconoce frases parecidas
              aunque tengan errores de dedo o de ortografía.
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1">
                <span className="text-[11px] text-slate-500">Mínimo</span>
                <RangeSlider id="param-ngram-min" min={1} max={params.ngramMax} value={params.ngramMin} onChange={setParam('ngramMin')} accent={accent} />
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-[11px] text-slate-500">Máximo</span>
                <RangeSlider id="param-ngram-max" min={params.ngramMin} max={8} value={params.ngramMax} onChange={setParam('ngramMax')} accent={accent} />
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-max-features">
              Vocabulario máximo: {params.maxFeatures.toLocaleString('es-MX')} fragmentos
            </Label>
            <p className="text-xs text-slate-500">
              Cuántos fragmentos de texto distintos puede llegar a aprender. Más alto puede ser más preciso, pero el
              entrenamiento tarda más.
            </p>
            <RangeSlider
              id="param-max-features"
              min={1000}
              max={50000}
              step={1000}
              value={params.maxFeatures}
              onChange={setParam('maxFeatures')}
              accent={accent}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-bottleneck">Nivel de detalle interno: {params.bottleneckDim}</Label>
            <p className="text-xs text-slate-500">
              Qué tan detallado es el resumen que la red neuronal hace de cada frase antes de agruparlas. Más alto
              captura más matices, pero también más ruido.
            </p>
            <RangeSlider
              id="param-bottleneck"
              min={10}
              max={300}
              step={10}
              value={params.bottleneckDim}
              onChange={setParam('bottleneckDim')}
              accent={accent}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-epochs">Cuántas veces repasa tus frases: {params.epochs}</Label>
            <p className="text-xs text-slate-500">
              La red neuronal aprende viendo tus frases varias veces seguidas. Más repasos suele aprender mejor, pero
              el entrenamiento tarda más.
            </p>
            <RangeSlider
              id="param-epochs"
              min={5}
              max={50}
              value={params.epochs}
              onChange={setParam('epochs')}
              accent={accent}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-k-min">
              Cuántos grupos buscar: entre {params.kMin} y {params.kMax}
            </Label>
            <p className="text-xs text-slate-500">
              El modelo prueba varias cantidades de grupos dentro de este rango y se queda con la que mejor separa tus
              frases.
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1">
                <span className="text-[11px] text-slate-500">Mínimo</span>
                <RangeSlider id="param-k-min" min={2} max={params.kMax} value={params.kMin} onChange={setParam('kMin')} accent={accent} />
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-[11px] text-slate-500">Máximo</span>
                <RangeSlider id="param-k-max" min={params.kMin} max={40} value={params.kMax} onChange={setParam('kMax')} accent={accent} />
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="param-contamination">
              Porcentaje esperado de frases raras o rotas: {params.contaminationPercent}%
            </Label>
            <p className="text-xs text-slate-500">
              Las frases que no se parecen a nada más se marcan como "Sin clasificar" en vez de forzarlas dentro de un
              grupo que no les corresponde.
            </p>
            <RangeSlider
              id="param-contamination"
              min={1}
              max={20}
              value={params.contaminationPercent}
              onChange={setParam('contaminationPercent')}
              accent={accent}
            />
          </div>
        </div>
      )}
    </div>
  )
}
