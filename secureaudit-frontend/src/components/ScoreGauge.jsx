/**
 * ScoreGauge.jsx — Circular security score gauge (0-100)
 * 
 * Displays a circular progress ring with the security score.
 * Color changes based on score:
 * - 90-100: emerald (excellent)
 * - 70-89:  green (good)
 * - 50-69:  yellow (fair)
 * - 30-49:  orange (poor)
 * - 0-29:   red (critical)
 */

function ScoreGauge({ score, label }) {
  /**
   * Calculate the stroke-dasharray for the SVG circle.
   * The circle has a circumference of ~283 (2 * PI * 45).
   * We fill it proportionally to the score.
   */
  const radius = 45
  const circumference = 2 * Math.PI * radius
  const filled = (score / 100) * circumference
  const empty = circumference - filled

  /**
   * Get color based on score value.
   * @returns {string} hex color code
   */
  const getColor = () => {
    if (score >= 90) return '#1D9E75'  // emerald
    if (score >= 70) return '#22c55e'  // green
    if (score >= 50) return '#eab308'  // yellow
    if (score >= 30) return '#f97316'  // orange
    return '#ef4444'                    // red
  }

  /**
   * Get text color class based on score.
   * @returns {string} Tailwind color class
   */
  const getTextColor = () => {
    if (score >= 90) return 'text-emerald-400'
    if (score >= 70) return 'text-green-400'
    if (score >= 50) return 'text-yellow-400'
    if (score >= 30) return 'text-orange-400'
    return 'text-red-400'
  }

  return (
    <div className="flex flex-col items-center gap-3">
      {/* SVG circular gauge */}
      <div className="relative w-32 h-32">
        <svg
          className="w-full h-full -rotate-90"
          viewBox="0 0 100 100"
        >
          {/* Background circle (gray track) */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="8"
          />
          {/* Foreground circle (score fill) */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={getColor()}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${filled} ${empty}`}
            style={{ transition: 'stroke-dasharray 0.8s ease' }}
          />
        </svg>

        {/* Score number in center */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-3xl font-bold ${getTextColor()}`}>
            {score}
          </span>
          <span className="text-slate-400 text-xs">/100</span>
        </div>
      </div>

      {/* Score label below */}
      {label && (
        <span className={`text-sm font-medium ${getTextColor()}`}>
          {label}
        </span>
      )}
    </div>
  )
}

export default ScoreGauge