import { useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { scanService } from '../services/scanService'
import Layout from '../components/Layout'
import ScoreGauge from '../components/ScoreGauge'
import FindingCard from '../components/FindingCard'

/**
 * ScanPage.jsx — Main scan page
 * 
 * Allows users to:
 * 1. Enter a URL and launch a security scan
 * 2. View the security score with a visual gauge
 * 3. See all findings with severity badges
 * 4. Expand each finding to see recommendations
 * 
 * Flow:
 * User enters URL → POST /api/scans → display score + findings
 */

function ScanPage() {
  const { isAuthenticated, token } = useAuth()
  const location = useLocation()

  // Pre-fill URL if coming from LandingPage
  const [url, setUrl] = useState(location.state?.url || '')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [scanResult, setScanResult] = useState(null)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  /**
   * Handle scan form submission.
   * Calls POST /api/scans and stores the result in state.
   */
  const handleScan = async (e) => {
    e.preventDefault()
    setError('')
    setScanResult(null)

    // Basic URL validation
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('Please enter a valid URL starting with http:// or https://')
      return
    }

    setLoading(true)

    try {
      const result = await scanService.createScan(url, token)
      setScanResult(result)
    } catch (err) {
      setError('Scan failed. Please check the URL and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-emerald-400 mb-6">
        New Scan
      </h1>

      {/* URL Input Form */}
      <form onSubmit={handleScan} className="flex gap-3 mb-8">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-medium px-6 py-3 rounded-lg transition whitespace-nowrap"
        >
          {loading ? 'Scanning...' : 'Scan now'}
        </button>
      </form>

      {/* Error message */}
      {error && (
        <div className="bg-red-900/30 border border-red-700 text-red-400 text-sm p-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-16 gap-4">
          <div className="w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-400 text-sm">
            Analyzing {url}...
          </p>
        </div>
      )}

      {/* Scan Results */}
      {scanResult && !loading && (
        <div className="space-y-6">

          {/* Score + Summary */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <div className="flex flex-col md:flex-row items-center gap-8">

              {/* Score gauge */}
              <ScoreGauge
                score={scanResult.score}
                label={scanResult.score_label}
              />

              {/* Summary info */}
              <div className="flex-1">
                <p className="text-slate-400 text-sm mb-1">Scanned URL</p>
                <p className="text-white font-medium mb-4 break-all">
                  {scanResult.url}
                </p>

                {/* Severity counts */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="bg-red-900/20 border border-red-800/50 rounded-lg p-3 text-center">
                    <p className="text-2xl font-bold text-red-400">
                      {scanResult.severity_counts?.critical || 0}
                    </p>
                    <p className="text-xs text-red-400 mt-1">Critical</p>
                  </div>
                  <div className="bg-orange-900/20 border border-orange-800/50 rounded-lg p-3 text-center">
                    <p className="text-2xl font-bold text-orange-400">
                      {scanResult.severity_counts?.medium || 0}
                    </p>
                    <p className="text-xs text-orange-400 mt-1">Medium</p>
                  </div>
                  <div className="bg-blue-900/20 border border-blue-800/50 rounded-lg p-3 text-center">
                    <p className="text-2xl font-bold text-blue-400">
                      {scanResult.severity_counts?.low || 0}
                    </p>
                    <p className="text-xs text-blue-400 mt-1">Low</p>
                  </div>
                  <div className="bg-emerald-900/20 border border-emerald-800/50 rounded-lg p-3 text-center">
                    <p className="text-2xl font-bold text-emerald-400">
                      {scanResult.findings?.filter(f => f.status === 'pass').length || 0}
                    </p>
                    <p className="text-xs text-emerald-400 mt-1">Passed</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Findings list */}
          <div>
            <h2 className="text-lg font-medium text-white mb-4">
              Detailed Findings ({scanResult.findings?.length || 0} checks)
            </h2>
            <div className="space-y-3">
              {scanResult.findings?.map((finding) => (
                <FindingCard
                  key={finding.id}
                  finding={finding}
                />
              ))}
            </div>
          </div>

        </div>
      )}
    </Layout>
  )
}

export default ScanPage