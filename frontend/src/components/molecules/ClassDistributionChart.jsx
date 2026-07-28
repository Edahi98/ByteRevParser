import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLayerGroup } from '@fortawesome/free-solid-svg-icons'
import { ChartCard } from './ChartCard'
import { CHART_PALETTE } from '../../data/chartTheme'

export function ClassDistributionChart({ classes }) {
  return (
    <ChartCard title="Distribución de clases en el dataset" icon={<FontAwesomeIcon icon={faLayerGroup} />}>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={classes} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#a7f3d0" opacity={0.5} />
            <XAxis dataKey="etiqueta" tick={{ fontSize: 12, fill: '#78716c' }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: '#78716c' }} />
            <Tooltip
              contentStyle={{ borderRadius: 10, borderColor: '#6ee7b7', fontSize: 12 }}
              labelStyle={{ fontWeight: 600, color: '#065f46' }}
            />
            <Bar dataKey="conteo" name="Ejemplos" radius={[8, 8, 0, 0]}>
              {classes.map((entry, index) => (
                <Cell key={entry.etiqueta} fill={CHART_PALETTE[index % CHART_PALETTE.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  )
}
