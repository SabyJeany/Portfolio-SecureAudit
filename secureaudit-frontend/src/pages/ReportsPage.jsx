import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Layout from '../components/Layout'

function ReportsPage() {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-emerald-400 mb-6">PDF Reports</h1>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <p className="text-slate-300">📄 PDF Reports — coming soon</p>
      </div>
    </Layout>
  )
}

export default ReportsPage