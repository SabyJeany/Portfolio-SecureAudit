/**
 * FindingCard.jsx — Card displaying a single security finding
 * 
 * Shows:
 * - Check name and severity badge
 * - Status (pass/fail)
 * - Description of what was found
 * - Recommendation on how to fix it (expandable)
 */

import { useState } from 'react'
import SeverityBadge from './SeverityBadge'

function FindingCard({ finding }) {
  /**
   * Toggle expanded state to show/hide recommendation.
   */
  const [expanded, setExpanded] = useState(false)

  /**
   * Get background color based on status and severity.
   * @returns {string} Tailwind CSS classes
   */
  const getCardStyle = () => {
    if (finding.status === 'pass') {
      return 'border-emerald-800/50 bg-emerald-900/10'
    }
    switch (finding.severity) {
      case 'critical':
        return 'border-red-800/50 bg-red-900/10'
      case 'medium':
        return 'border-orange-800/50 bg-orange-900/10'
      case 'low':
        return 'border-blue-800/50 bg-blue-900/10'
      default:
        return 'border-slate-700 bg-slate-800/50'
    }
  }

  return (
    <div className={`border rounded-xl p-4 transition ${getCardStyle()}`}>
      
      {/* Header: check name + badge */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          {/* Status icon */}
          <span className="text-lg">
            {finding.status === 'pass' ? '✅' : '❌'}
          </span>
          {/* Check name */}
          <span className="text-white font-medium text-sm">
            {finding.check_name}
          </span>
        </div>
        {/* Severity badge */}
        <SeverityBadge
          severity={finding.severity}
          status={finding.status}
        />
      </div>

      {/* Description */}
      {finding.description && (
        <p className="text-slate-400 text-sm mb-3 ml-8">
          {finding.description}
        </p>
      )}

      {/* Recommendation — only show for failed checks */}
      {finding.status === 'fail' && finding.recommendation && (
        <div className="ml-8">
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-slate-500 hover:text-slate-300 transition flex items-center gap-1"
          >
            <span>{expanded ? '▾' : '▸'}</span>
            <span>{expanded ? 'Hide recommendation' : 'View recommendation'}</span>
          </button>

          {expanded && (
            <div className="mt-2 bg-slate-900 border border-slate-700 rounded-lg p-3">
              <p className="text-xs text-slate-300 font-mono">
                {finding.recommendation}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FindingCard