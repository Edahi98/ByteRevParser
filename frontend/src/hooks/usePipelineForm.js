import { useDispatch, useSelector } from 'react-redux'
import {
  artifactsSelected,
  documentSelected,
  pipelineFormReset,
  pipelineLoaded,
  schemaFieldsChanged,
  selectArtifactsFile,
  selectDocumentFile,
  selectIsPipelineFormDirty,
  selectIsPipelineFormReady,
  selectPipelineContent,
  selectPipelineFileName,
  selectSchemaFields,
  selectSchemaJson,
} from '../store/pipelineFormSlice'
import { useFileText } from './useFileText'

export function usePipelineForm() {
  const dispatch = useDispatch()

  const file = useSelector(selectDocumentFile)
  const artifacts = useSelector(selectArtifactsFile)
  const pipeline = useSelector(selectPipelineContent)
  const pipelineFileName = useSelector(selectPipelineFileName)
  const schemaFields = useSelector(selectSchemaFields)
  const schema = useSelector(selectSchemaJson)
  const isReady = useSelector(selectIsPipelineFormReady)
  const isDirty = useSelector(selectIsPipelineFormDirty)

  // El nombre solo se guarda cuando el contenido ya se leyó, para que no pueda
  // mostrarse un archivo "cargado" con el pipeline todavía en null.
  const loadPipelineFile = useFileText((content, pipelineFile) =>
    dispatch(pipelineLoaded({ content, fileName: pipelineFile.name })),
  )

  return {
    file,
    artifacts,
    pipeline,
    pipelineFileName,
    schemaFields,
    schema,
    isReady,
    isDirty,
    selectDocument: (documentFile) => dispatch(documentSelected(documentFile)),
    selectArtifacts: (artifactsFile) => dispatch(artifactsSelected(artifactsFile)),
    loadPipelineFile,
    changeSchemaFields: (fields) => dispatch(schemaFieldsChanged(fields)),
    resetForm: () => dispatch(pipelineFormReset()),
  }
}
