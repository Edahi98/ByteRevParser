import { Header } from '../components/organisms/Header'
import { PipelineForm } from '../components/organisms/PipelineForm'
import { DeveloperOptionsPanel } from '../components/organisms/DeveloperOptionsPanel'
import { ResultPanel } from '../components/organisms/ResultPanel'
import { MainTemplate } from '../components/templates/MainTemplate'
import { useExecutePipeline } from '../hooks/useExecutePipeline'

export function HomePage() {
  const { execute, result, error, isLoading } = useExecutePipeline()

  return (
    <MainTemplate
      header={<Header title="RedDragon" subtitle="Sube tu documento y obtén los datos de su control de cambios al instante" />}
    >
      <PipelineForm onSubmit={execute} isLoading={isLoading}>
        {(developerProps) => <DeveloperOptionsPanel {...developerProps} />}
      </PipelineForm>
      <ResultPanel result={result} error={error} isLoading={isLoading} />
    </MainTemplate>
  )
}
