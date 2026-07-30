import { Header } from '../components/organisms/Header'
import { TrainDetectorCambiosForm } from '../components/organisms/TrainDetectorCambiosForm'
import { DetectorCambiosMetricsDashboard } from '../components/organisms/DetectorCambiosMetricsDashboard'
import { CompareCambioForm } from '../components/organisms/CompareCambioForm'
import { CompareCambioBatchForm } from '../components/organisms/CompareCambioBatchForm'
import { MainTemplate } from '../components/templates/MainTemplate'
import { useTrainDetectorCambios } from '../hooks/useTrainDetectorCambios'
import { useCompareCambio } from '../hooks/useCompareCambio'
import { useCompareCambioBatch } from '../hooks/useCompareCambioBatch'

export function DetectorCambiosPage() {
  const { train, report, archive, error: trainError, isLoading: isTraining } = useTrainDetectorCambios()
  const { compare, result, error: compareError, isLoading: isComparing } = useCompareCambio()
  const {
    compareBatch,
    resultados,
    error: compareBatchError,
    isLoading: isComparingBatch,
  } = useCompareCambioBatch()

  return (
    <MainTemplate
      header={<Header title="ByteRevParser" subtitle="Detector de cambios · Core API Services" accent="green" />}
    >
      <div 
        className="w-full py-10 md:py-14 bg-cover bg-center bg-no-repeat bg-fixed"
        style={{
          backgroundImage: "linear-gradient(to bottom, rgba(236, 253, 245, 0.4), rgba(240, 249, 255, 0.6), rgba(255, 255, 255, 0.9)), url('/bg-compare.png')"
        }}
      >
        <div className="max-w-5xl mx-auto px-4 md:px-6 flex flex-col gap-6">
          <TrainDetectorCambiosForm onSubmit={train} isLoading={isTraining} error={trainError} />
          <DetectorCambiosMetricsDashboard report={report} archive={archive} />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            <CompareCambioForm
              onSubmit={compare}
              isLoading={isComparing}
              result={result}
              error={compareError}
              quickArchive={archive}
            />
            <CompareCambioBatchForm
              onSubmit={compareBatch}
              isLoading={isComparingBatch}
              resultados={resultados}
              error={compareBatchError}
              quickArchive={archive}
            />
          </div>
        </div>
      </div>
    </MainTemplate>
  )
}
