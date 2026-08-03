import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { store } from './store/store'
import { hydratePipelineForm, startPipelineFormPersistence } from './store/pipelineFormPersistence'

// Se rehidrata antes del primer render para que el formulario no aparezca vacío
// y se rellene un instante después.
hydratePipelineForm(store).then(() => {
  startPipelineFormPersistence(store)

  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    </StrictMode>,
  )
})
