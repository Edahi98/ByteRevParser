import { Route, Routes } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { TextClassifierPage } from './pages/TextClassifierPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/clasificador-texto" element={<TextClassifierPage />} />
    </Routes>
  )
}

export default App
