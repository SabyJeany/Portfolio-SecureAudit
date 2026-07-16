/**
 * DashboardPage.jsx — Main dashboard with real scan statistics
 * 
 * Displays:
 * - Last scan summary (score + URL)
 * - Total scans count
 * - Quick scan button
 */

import { useState, useEffect } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { scanService } from '../services/scanService'
import Layout from '../components/Layout'
import ScoreGauge from '../components/ScoreGauge'

function DashboardPage() {
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const data = await scanService.getScans(token)
        setScans(data)
      } catch (err) {
        console.error('Could not load scans', err)
      } finally {
        setLoading(false)
      }
    }
    fetchScans()
  }, [token])

  const lastScan = scans[0] || null

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-emerald-400 mb-6">
        Dashboard
      </h1>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="space-y-6">

          {/* Stats row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm mb-1">Total scans</p>
              <p className="text-3xl font-bold text-white">{scans.length}</p>
            </div>
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm mb-1">Last score</p>
              <p className={`text-3xl font-bold ${
                lastScan
                  ? lastScan.score >= 70 ? 'text-emerald-400'
                  : lastScan.score >= 50 ? 'text-yellow-400'
                  : 'text-orange-400'
                  : 'text-slate-500'
              }`}>
                {lastScan ? `${lastScan.score}/100` : '—'}
              </p>
            </div>
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm mb-1">Last label</p>
              <p className="text-3xl font-bold text-white">
                {lastScan ? lastScan.score_label : '—'}
              </p>
            </div>
          </div>

          {/* Last scan detail */}
          {lastScan ? (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-lg font-medium text-white mb-4">
                Last scan
              </h2>
              <div className="flex flex-col md:flex-row items-center gap-8">
                <ScoreGauge
                  score={lastScan.score}
                  label={lastScan.score_label}
                />
                <div className="flex-1">
                  <p className="text-slate-400 text-sm mb-1">URL</p>
                  <p className="text-white font-medium mb-3">{lastScan.url}</p>
                  <p className="text-slate-400 text-sm mb-1">Date</p>
                  <p className="text-white text-sm mb-4">
                    {new Date(lastScan.created_at).toLocaleDateString('en-GB', {
                      day: '2-digit', month: 'short', year: 'numeric',
                      hour: '2-digit', minute: '2-digit'
                    })}
                  </p>
                  <button
                    onClick={() => navigate('/history')}
                    className="text-emerald-400 hover:text-emerald-300 text-sm transition"
                  >
                    View all scans →
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-12 text-center">
              <p className="text-slate-400 text-lg mb-2">No scans yet</p>
              <p className="text-slate-500 text-sm mb-6">
                Run your first scan to see your security score.
              </p>
              <button
                onClick={() => navigate('/scan')}
                className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg text-sm transition"
              >
                Start a scan
              </button>
            </div>
          )}

        </div>
      )}
    </Layout>
  )
}

export default DashboardPage