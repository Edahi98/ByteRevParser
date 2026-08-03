import { createSelector, createSlice } from '@reduxjs/toolkit'
import { DEFAULT_SCHEMA_FIELDS } from '../data/defaultSchemaFields'

const initialState = {
  document: { file: null },
  artifacts: { file: null },
  pipeline: { content: null, fileName: null },
  schema: { fields: DEFAULT_SCHEMA_FIELDS },
}

const pipelineFormSlice = createSlice({
  name: 'pipelineForm',
  initialState,
  reducers: {
    documentSelected(state, action) {
      state.document.file = action.payload ?? null
    },
    artifactsSelected(state, action) {
      state.artifacts.file = action.payload ?? null
    },
    pipelineLoaded(state, action) {
      state.pipeline.content = action.payload.content
      state.pipeline.fileName = action.payload.fileName
    },
    schemaFieldsChanged(state, action) {
      state.schema.fields = action.payload
    },
    // Se reconstruye campo a campo en lugar de aceptar el payload tal cual:
    // lo persistido puede venir de una forma anterior del estado.
    pipelineFormRehydrated(state, action) {
      const saved = action.payload ?? {}
      const fields = saved.schema?.fields

      return {
        document: { file: saved.document?.file ?? null },
        artifacts: { file: saved.artifacts?.file ?? null },
        pipeline: {
          content: saved.pipeline?.content ?? null,
          fileName: saved.pipeline?.fileName ?? null,
        },
        schema: {
          fields: Array.isArray(fields) && fields.length > 0 ? fields : DEFAULT_SCHEMA_FIELDS,
        },
      }
    },
    pipelineFormReset() {
      return initialState
    },
  },
})

export const {
  documentSelected,
  artifactsSelected,
  pipelineLoaded,
  schemaFieldsChanged,
  pipelineFormRehydrated,
  pipelineFormReset,
} = pipelineFormSlice.actions
export const pipelineFormReducer = pipelineFormSlice.reducer

export const selectDocumentFile = (state) => state.pipelineForm.document.file
export const selectArtifactsFile = (state) => state.pipelineForm.artifacts.file
export const selectPipelineContent = (state) => state.pipelineForm.pipeline.content
export const selectPipelineFileName = (state) => state.pipelineForm.pipeline.fileName
export const selectSchemaFields = (state) => state.pipelineForm.schema.fields

// Los derivados se memoizan con createSelector porque devuelven referencias
// nuevas (array / string) y sin memoizar dispararían un re-render por cada
// despacho, aunque los campos no hayan cambiado.
export const selectValidSchemaFields = createSelector([selectSchemaFields], (fields) =>
  fields.map((field) => field.trim()).filter((field) => field.length > 0),
)

export const selectSchemaJson = createSelector([selectValidSchemaFields], (fields) =>
  JSON.stringify(Object.fromEntries(fields.map((field) => [field, ''])), null, 2),
)

// El ZIP del detector es obligatorio: sin él el backend no puede filtrar el
// resultado de Tsubasa y `/execute_pipeline` responde 422.
export const selectIsPipelineFormReady = createSelector(
  [selectDocumentFile, selectArtifactsFile, selectPipelineContent, selectValidSchemaFields],
  (file, artifacts, pipeline, fields) =>
    Boolean(file) && Boolean(artifacts) && Boolean(pipeline) && fields.length > 0,
)

// Habilita el botón de limpiar: sin esto seguiría activo sobre un formulario
// que ya está en su estado inicial.
export const selectIsPipelineFormDirty = createSelector(
  [selectDocumentFile, selectArtifactsFile, selectPipelineContent, selectSchemaFields],
  (file, artifacts, pipeline, fields) =>
    Boolean(file) ||
    Boolean(artifacts) ||
    Boolean(pipeline) ||
    fields.length !== DEFAULT_SCHEMA_FIELDS.length ||
    fields.some((field, index) => field !== DEFAULT_SCHEMA_FIELDS[index]),
)
