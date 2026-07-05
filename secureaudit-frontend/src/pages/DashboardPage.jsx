import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function DashboardPage() {
  const { isAuthenticated, user, logout } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-semibold text-emerald-400">SECUREAUDIT — Dashboard</h1>
        <button
          onClick={logout}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg text-sm"
        >
          Log out
        </button>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <p className="text-slate-300">
          🎉 You are logged in! This is a protected route — only visible when authenticated.
        </p>
      </div>
    </div>
  )
}

export default DashboardPage