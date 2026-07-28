import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartPie } from '@fortawesome/free-solid-svg-icons'
import { ChartCard } from './ChartCard'
import { CHART_PALETTE } from '../../data/chartTheme'

function countByLabel(predictions) {
  const counts = new Map()
  predictions.forEach(({ etiqueta }) => {
    counts.set(etiqueta, (counts.get(etiqueta) || 0) + 1)
  })
  return Array.from(counts, ([etiqueta, conteo]) => ({ etiqueta, conteo }))
}

export function PredictionsDistributionChart({ predictions }) {
  const data = countByLabel(predictions)

  return (
    <ChartCard title="Distribución de las predicciones" icon={<FontAwesomeIcon icon={faChartPie} />}>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="conteo" nameKey="etiqueta" innerRadius={45} outerRadius={80} paddingAngle={3}>
              {data.map((entry, index) => (
                <Cell key={entry.etiqueta} fill={CHART_PALETTE[index % CHART_PALETTE.length]} />
              ))}
            </Pie>
            <Tooltip contentStyle={{ borderRadius: 10, borderColor: '#5eead4', fontSize: 12 }} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  )
}
