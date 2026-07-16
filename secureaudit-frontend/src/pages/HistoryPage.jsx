/**
 * HistoryPage.jsx — Scan history page
 * 
 * Displays all scans performed by the logged-in user.
 * Shows: URL, date, score, score label, severity counts.
 * Allows clicking on a scan to view its full report.
 */

import { useState, useEffect } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { scanService } from '../services/scanService'
import Layout from '../components/Layout'
import SeverityBadge from '../components/SeverityBadge'

function HistoryPage() {
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  /**
   * Fetch scan history on component mount.
   */
  useEffect(() => {
    const fetchScans = async () => {
      try {
        const data = await scanService.getScans(token)
        setScans(data)
      } catch (err) {
        setError('Could not load scan history.')
      } finally {
        setLoading(false)
      }
    }

    fetchScans()
  }, [token])

  /**
   * Get score color class based on score value.
   * @param {number} score
   * @returns {string} Tailwind color class
   */
  const getScoreColor = (score) => {
    if (score >= 90) return 'text-emerald-400'
    if (score >= 70) return 'text-green-400'
    if (score >= 50) return 'text-yellow-400'
    if (score >= 30) return 'text-orange-400'
    return 'text-red-400'
  }

  /**
   * Format date to readable string.
   * @param {string} dateString
   * @returns {string} formatted date
   */
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-emerald-400 mb-6">
        Scan History
      </h1>

      {/* Loading state */}
      {loading && (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="bg-red-900/30 border border-red-700 text-red-400 text-sm p-4 rounded-lg">
          {error}
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && scans.length === 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-12 text-center">
          <p className="text-slate-400 text-lg mb-2">No scans yet</p>
          <p className="text-slate-500 text-sm mb-6">
            Run your first scan to see results here.
          </p>
          <button
            onClick={() => navigate('/scan')}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg text-sm transition"
          >
            Start a scan
          </button>
        </div>
      )}

      {/* Scans table */}
      {!loading && scans.length > 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700 bg-slate-900/50">
                <th className="text-left text-slate-400 text-xs font-medium px-4 py-3 uppercase tracking-wider">URL</th>
                <th className="text-left text-slate-400 text-xs font-medium px-4 py-3 uppercase tracking-wider">Date</th>
                <th className="text-center text-slate-400 text-xs font-medium px-4 py-3 uppercase tracking-wider">Score</th>
                <th className="text-center text-slate-400 text-xs font-medium px-4 py-3 uppercase tracking-wider">Label</th>
              </tr>
            </thead>
            <tbody>
              {scans.map((scan, index) => (
                <tr
                  key={scan.id}
                  onClick={() => navigate(`/scan/${scan.id}`)}
                  className={`
                    border-b border-slate-700/50 cursor-pointer
                    hover:bg-slate-700/30 transition
                    ${index % 2 === 0 ? 'bg-slate-800' : 'bg-slate-800/50'}
                  `}
                >
                  <td className="px-4 py-3">
                    <p className="text-white text-sm truncate max-w-xs">
                      {scan.url}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-slate-400 text-sm">
                      {formatDate(scan.created_at)}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-lg font-bold ${getScoreColor(scan.score)}`}>
                      {scan.score}
                    </span>
                    <span className="text-slate-500 text-xs">/100</span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-sm font-medium ${getScoreColor(scan.score)}`}>
                      {scan.score_label}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  )
}

export default HistoryPage