import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function LandingPage() {
  const [url, setUrl] = useState('')
  const [error, setError] = useState('')
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const handleScan = (e) => {
    e.preventDefault()
    setError('')

    // Basic URL validation

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('Please enter a valid URL starting with http:// or https://')
      return
    }

    // If authenticated → redirect to scan page with the URL
    if (isAuthenticated) {
      navigate('/scan', { state: { url } })
    } else {
      // If not authenticated → redirect to login
      navigate('/login')
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 px-8 py-4 flex items-center justify-between">
        <span className="text-emerald-400 font-semibold text-lg tracking-widest">
          SECURE<span className="text-white">AUDIT</span>
        </span>
        <div className="flex gap-4">
          <a href="/login" className="text-slate-400 hover:text-white text-sm transition">
            Log in
          </a>
          <a href="/login" className="bg-emerald-600 hover:bg-emerald-700 text-white text-sm px-4 py-2 rounded-lg transition">
            Get started
          </a>
        </div>
      </header>

      {/* Hero */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 text-center">
        <div className="mb-6 bg-emerald-900/30 border border-emerald-700 text-emerald-400 text-sm px-4 py-2 rounded-full">
          Web security audit — automated
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 leading-tight">
          Analyze your site security<br />
          in <span className="text-emerald-400">less than 10 seconds</span>
        </h1>

        <p className="text-slate-400 text-lg mb-10 max-w-xl">
          No technical skills needed. Enter a URL, get a clear report with score and recommendations.
        </p>

        {/* URL Input */}
        <form onSubmit={handleScan} className="w-full max-w-xl flex gap-3 mb-4">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
          <button
            type="submit"
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-6 py-3 rounded-lg transition whitespace-nowrap"
          >
            Scan now
          </button>
        </form>

        {error && (
          <p className="text-red-400 text-sm mb-4">{error}</p>
        )}

        {/* 3 steps */}
        <div className="flex items-center gap-6 text-sm text-slate-400 mt-4">
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-emerald-900 text-emerald-400 flex items-center justify-center text-xs font-bold">1</span>
            Enter URL
          </div>
          <span className="text-slate-600">→</span>
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-emerald-900 text-emerald-400 flex items-center justify-center text-xs font-bold">2</span>
            Scan runs
          </div>
          <span className="text-slate-600">→</span>
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-emerald-900 text-emerald-400 flex items-center justify-center text-xs font-bold">3</span>
            Get report
          </div>
        </div>
      </main>
    </div>
  )
}

export default LandingPage