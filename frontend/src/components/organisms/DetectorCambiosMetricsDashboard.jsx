import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircleCheck } from '@fortawesome/free-solid-svg-icons'
import { GradientCard } from '../molecules/GradientCard'
import { DownloadArtifactsButton } from '../molecules/DownloadArtifactsButton'

export function DetectorCambiosMetricsDashboard({ report, archive }) {
  if (!report) return null

  return (
    <GradientCard icon={<FontAwesomeIcon icon={faCircleCheck} />} title="Listo" gradient="sky">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-sm text-slate-600">Ya puedes usarlo.</span>
        {archive && <DownloadArtifactsButton archive={archive} />}
      </div>
    </GradientCard>
  )
}
