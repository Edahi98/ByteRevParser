import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartLine } from '@fortawesome/free-solid-svg-icons'
import { ChartCard } from './ChartCard'
import { MODEL_COLORS, MODEL_LABELS } from '../../data/chartTheme'

export function CrossValidationChart({ resultsCv }) {
  const modelKeys = Object.keys(resultsCv)
  const foldCount = modelKeys.length > 0 ? resultsCv[modelKeys[0]].f1_macro_por_fold.length : 0

  const data = Array.from({ length: foldCount }, (_, foldIndex) => {
    const point = { fold: `Fold ${foldIndex + 1}` }
    modelKeys.forEach((modelKey) => {
      point[modelKey] = Number(resultsCv[modelKey].f1_macro_por_fold[foldIndex].toFixed(4))
    })
    return point
  })

  return (
    <ChartCard title="F1-macro por fold" icon={<FontAwesomeIcon icon={faChartLine} />}>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#a7f3d0" opacity={0.5} />
            <XAxis dataKey="fold" tick={{ fontSize: 12, fill: '#78716c' }} />
            <YAxis domain={[0, 1]} tick={{ fontSize: 12, fill: '#78716c' }} />
            <Tooltip contentStyle={{ borderRadius: 10, borderColor: '#6ee7b7', fontSize: 12 }} />
            <Legend
              formatter={(value) => MODEL_LABELS[value] || value}
              wrapperStyle={{ fontSize: 12 }}
            />
            {modelKeys.map((modelKey) => (
              <Line
                key={modelKey}
                type="monotone"
                dataKey={modelKey}
                name={modelKey}
                stroke={MODEL_COLORS[modelKey] || '#10b981'}
                strokeWidth={2.5}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  )
}
