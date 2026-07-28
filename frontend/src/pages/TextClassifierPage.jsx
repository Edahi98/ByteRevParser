import { Header } from '../components/organisms/Header'
import { TrainClassifierForm } from '../components/organisms/TrainClassifierForm'
import { ClassifierMetricsDashboard } from '../components/organisms/ClassifierMetricsDashboard'
import { SingleClassifyForm } from '../components/organisms/SingleClassifyForm'
import { BatchClassifyForm } from '../components/organisms/BatchClassifyForm'
import { MainTemplate } from '../components/templates/MainTemplate'
import { useTrainTextClassifier } from '../hooks/useTrainTextClassifier'
import { useClassifyText } from '../hooks/useClassifyText'
import { useClassifyTextBatch } from '../hooks/useClassifyTextBatch'

export function TextClassifierPage() {
  const { train, report, archive, error: trainError, isLoading: isTraining } = useTrainTextClassifier()
  const { classify, result, error: classifyError, isLoading: isClassifying } = useClassifyText()
  const {
    classifyBatch,
    predictions,
    error: classifyBatchError,
    isLoading: isClassifyingBatch,
  } = useClassifyTextBatch()

  return (
    <MainTemplate
      header={
        <Header
          title="RedDragon"
          subtitle="Crea tus propios clasificadores de texto, con las clases que tú definas"
          accent="green"
        />
      }
    >
      <TrainClassifierForm onSubmit={train} isLoading={isTraining} error={trainError} />
      <ClassifierMetricsDashboard report={report} archive={archive} />
      <SingleClassifyForm
        onSubmit={classify}
        isLoading={isClassifying}
        result={result}
        error={classifyError}
        quickArchive={archive}
      />
      <BatchClassifyForm
        onSubmit={classifyBatch}
        isLoading={isClassifyingBatch}
        predictions={predictions}
        error={classifyBatchError}
        quickArchive={archive}
      />
    </MainTemplate>
  )
}
