import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartSimple, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FormSection } from '../molecules/FormSection'
import { ClassDistributionChart } from '../molecules/ClassDistributionChart'
import { ModelComparisonChart } from '../molecules/ModelComparisonChart'
import { CrossValidationChart } from '../molecules/CrossValidationChart'
import { ClassificationReportTable } from '../molecules/ClassificationReportTable'
import { DownloadArtifactsButton } from '../molecules/DownloadArtifactsButton'

const EXPORTED_MODEL_KEY = 'RandomForestClassifier'

export function ClassifierMetricsDashboard({ report, archive }) {
  if (!report) return null

  const exportedModelReport = report.resultados_cv[EXPORTED_MODEL_KEY]

  return (
    <FormSection
      title="Así quedó tu modelo"
      icon={<FontAwesomeIcon icon={faChartSimple} />}
      accent="emerald"
      subtitle="Un vistazo a qué tan bien aprendió tu modelo a distinguir cada clase"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 -mt-2">
        <span className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold px-3 py-1.5 rounded-full">
          <FontAwesomeIcon icon={faCheck} /> ¡Tu modelo está listo!
        </span>
        {archive && <DownloadArtifactsButton archive={archive} />}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <ClassDistributionChart classes={report.clases} />
        <ModelComparisonChart resultsCv={report.resultados_cv} />
      </div>

      <CrossValidationChart resultsCv={report.resultados_cv} />

      {exportedModelReport && (
        <div className="flex flex-col gap-2">
          <p className="text-xs font-semibold text-emerald-800">Qué tan bien clasifica cada clase</p>
          <ClassificationReportTable classificationReport={exportedModelReport.classification_report} />
        </div>
      )}
    </FormSection>
  )
}
