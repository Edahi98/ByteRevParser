import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartLine } from '@fortawesome/free-solid-svg-icons'
import { ChartCard } from './ChartCard'

export function SilhouetteChart({ silhouettePorK, kElegido }) {
  const data = Object.entries(silhouettePorK)
    .map(([k, puntaje]) => ({ k: Number(k), puntaje: Number(puntaje.toFixed(4)) }))
    .sort((a, b) => a.k - b.k)

  return (
    <ChartCard title="Qué tan bien separado queda cada número de grupos probado" icon={<FontAwesomeIcon icon={faChartLine} />}>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#99f6e4" opacity={0.5} />
            <XAxis dataKey="k" tick={{ fontSize: 12, fill: '#78716c' }} label={{ value: 'Número de grupos (K)', position: 'insideBottom', offset: -2, fontSize: 11, fill: '#78716c' }} />
            <YAxis domain={[-1, 1]} tick={{ fontSize: 12, fill: '#78716c' }} />
            <Tooltip
              contentStyle={{ borderRadius: 10, borderColor: '#5eead4', fontSize: 12 }}
              labelFormatter={(k) => `K = ${k}`}
              formatter={(value) => [value, 'Silhouette']}
            />
            <Bar dataKey="puntaje" name="Silhouette" radius={[8, 8, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.k} fill={entry.k === kElegido ? '#10b981' : '#99f6e4'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  )
}
