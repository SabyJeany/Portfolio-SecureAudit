import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import AuthPage from './pages/AuthPage'
import DashboardPage from './pages/DashboardPage'
import ScanPage from './pages/ScanPage'
import HistoryPage from './pages/HistoryPage'
import ReportsPage from './pages/ReportsPage'
import LandingPage from './pages/LandingPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/scan" element={<ScanPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App