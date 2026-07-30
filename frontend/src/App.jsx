import { Route, Routes } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { DetectorCambiosPage } from './pages/DetectorCambiosPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/control-de-cambios" element={<DetectorCambiosPage />} />
    </Routes>
  )
}

export default App
