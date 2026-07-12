import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Layout from '../components/Layout'

function HistoryPage() {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-emerald-400 mb-6">History</h1>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <p className="text-slate-300">🕐 Scan history — coming soon</p>
      </div>
    </Layout>
  )
}

export default HistoryPage