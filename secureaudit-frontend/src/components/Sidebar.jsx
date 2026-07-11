import {NavLink} from 'react-router-dom'

const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊'},
    { path: '/scan/', label: 'New Scan', icon: '🔍' },
    { path: '/history', label: 'History', icon: '🕒' },
    { path: '/reports', label: 'PDF Reports', icon: '📄' },
]

function Sidebar() {
    return (
        <aside className="w-48 min-h-screen bg-slate-900 border-r border-slate-700 py-6">
            <nav className="flex flex-col">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-4 py-3 text-sm transition
                        ${isActive
                            ? 'text-emerald-400 bg-emerald-900/20 border-l-2 border-emerald-400'
                            : 'text-slate-400 hover:text-white hover:bg-slate-800'
                        }`
                        }
                    >
                        <span>{item.icon}</span>
                        <span>{item.label}</span>
                    </NavLink>
                ))}
            </nav>
        </aside>
    )
}

export default Sidebar