import { Bar, BarChart, CartesianGrid, Cell, ErrorBar, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faScaleBalanced } from '@fortawesome/free-solid-svg-icons'
import { ChartCard } from './ChartCard'
import { MODEL_COLORS, MODEL_LABELS } from '../../data/chartTheme'

export function ModelComparisonChart({ resultsCv }) {
  const data = Object.entries(resultsCv).map(([modelKey, metrics]) => ({
    modelKey,
    name: MODEL_LABELS[modelKey] || modelKey,
    f1: Number(metrics.f1_macro_promedio.toFixed(4)),
    desviacion: Number(metrics.f1_macro_desviacion.toFixed(4)),
  }))

  return (
    <ChartCard title="F1-macro promedio por modelo (validación cruzada)" icon={<FontAwesomeIcon icon={faScaleBalanced} />}>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#99f6e4" opacity={0.5} />
            <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#78716c' }} />
            <YAxis domain={[0, 1]} tick={{ fontSize: 12, fill: '#78716c' }} />
            <Tooltip
              contentStyle={{ borderRadius: 10, borderColor: '#5eead4', fontSize: 12 }}
              labelStyle={{ fontWeight: 600, color: '#115e59' }}
              formatter={(value, key) => [value, key === 'f1' ? 'F1-macro' : key]}
            />
            <Bar dataKey="f1" name="F1-macro" radius={[8, 8, 0, 0]}>
              <ErrorBar dataKey="desviacion" width={4} strokeWidth={2} stroke="#78716c" />
              {data.map((entry) => (
                <Cell key={entry.modelKey} fill={MODEL_COLORS[entry.modelKey] || '#10b981'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  )
}
