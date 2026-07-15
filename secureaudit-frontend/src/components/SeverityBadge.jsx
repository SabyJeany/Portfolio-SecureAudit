/**
 * SeverityBadge.jsx — Colored badge indicating finding severity
*/

function SeverityBadge({ severity, status }) {
  /**
   * Get Tailwind classes based on severity or status.
   * @returns {string} Tailwind CSS classes
   */
  const getStyles = () => {
    // If status is pass, always show green
    if (status === 'pass') {
      return 'bg-emerald-900/30 text-emerald-400 border border-emerald-700'
    }

    // Otherwise base on severity
    switch (severity) {
      case 'critical':
        return 'bg-red-900/30 text-red-400 border border-red-700'
      case 'medium':
        return 'bg-orange-900/30 text-orange-400 border border-orange-700'
      case 'low':
        return 'bg-blue-900/30 text-blue-400 border border-blue-700'
      case 'info':
        return 'bg-emerald-900/30 text-emerald-400 border border-emerald-700'
      default:
        return 'bg-slate-700 text-slate-300 border border-slate-600'
    }
  }

  /**
   * Get display label based on status or severity.
   * @returns {string} label to display
   */
  const getLabel = () => {
    if (status === 'pass') return 'Pass'
    return severity.charAt(0).toUpperCase() + severity.slice(1)
  }

  return (
    <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${getStyles()}`}>
      {getLabel()}
    </span>
  )
}

export default SeverityBadge