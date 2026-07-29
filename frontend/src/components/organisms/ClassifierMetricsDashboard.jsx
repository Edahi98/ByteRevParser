import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartSimple, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FormSection } from '../molecules/FormSection'
import { ClassDistributionChart } from '../molecules/ClassDistributionChart'
import { SilhouetteChart } from '../molecules/SilhouetteChart'
import { ClusterSummaryTable } from '../molecules/ClusterSummaryTable'
import { DownloadArtifactsButton } from '../molecules/DownloadArtifactsButton'
import { UsedConfigSummary } from '../molecules/UsedConfigSummary'

export function ClassifierMetricsDashboard({ report, archive }) {
  if (!report) return null

  const distribucionClusters = report.clusters.map((cluster) => ({
    etiqueta: `Grupo ${cluster.cluster_id}`,
    conteo: cluster.tamano,
  }))

  return (
    <FormSection
      title="Así quedó tu modelo"
      icon={<FontAwesomeIcon icon={faChartSimple} />}
      accent="emerald"
      subtitle="Un vistazo a los grupos que tu modelo descubrió solo, sin que tú los definieras"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 -mt-2">
        <span className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold px-3 py-1.5 rounded-full">
          <FontAwesomeIcon icon={faCheck} /> ¡Tu modelo está listo! Encontró {report.clusters.length} grupos (K = {report.k_elegido}) y marcó {report.frases_ruido} frase(s) como ruido
        </span>
        {archive && <DownloadArtifactsButton archive={archive} />}
      </div>

      {report.configuracion_usada && <UsedConfigSummary configuracion={report.configuracion_usada} />}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <ClassDistributionChart classes={distribucionClusters} />
        <SilhouetteChart silhouettePorK={report.silhouette_por_k} kElegido={report.k_elegido} />
      </div>

      <div className="flex flex-col gap-2">
        <p className="text-xs font-semibold text-emerald-800">Qué caracteriza a cada grupo</p>
        <ClusterSummaryTable clusters={report.clusters} />
      </div>
    </FormSection>
  )
}
