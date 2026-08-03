import { configureStore } from '@reduxjs/toolkit'
import { pipelineFormReducer } from './pipelineFormSlice'

export const store = configureStore({
  reducer: {
    pipelineForm: pipelineFormReducer,
  },
  // El documento y el ZIP del detector son `File` del navegador: no son
  // serializables y tienen que llegar intactos al `FormData` de la petición,
  // así que se excluyen del serializableCheck de RTK en lugar de guardar solo
  // sus metadatos.
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [
          'pipelineForm/documentSelected',
          'pipelineForm/artifactsSelected',
          'pipelineForm/pipelineFormRehydrated',
        ],
        ignoredPaths: ['pipelineForm.document.file', 'pipelineForm.artifacts.file'],
      },
    }),
})
