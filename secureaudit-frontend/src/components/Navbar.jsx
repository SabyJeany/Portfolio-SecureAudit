import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'

function Navbar() {
  const { logout, user } = useAuth()

  return (
    <nav className="bg-slate-900 border-b border-slate-700 px-6 py-3 flex items-center justify-between">
      {/* Logo */}
      <Link to="/dashboard" className="text-emerald-400 font-semibold text-lg tracking-widest">
        SECURE<span className="text-white">AUDIT</span>
      </Link>

      {/* Right side */}
      <div className="flex items-center gap-4">
        {user && (
          <span className="text-slate-400 text-sm">{user.email}</span>
        )}
        <button
          onClick={logout}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm px-4 py-2 rounded-lg transition"
        >
          Log out
        </button>
      </div>
    </nav>
  )
}

export default Navbar