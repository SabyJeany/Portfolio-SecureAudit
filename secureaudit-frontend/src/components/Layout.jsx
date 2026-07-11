import Navbar from './Navbar'
import Sidebar from './Sidebar'

function Layout({ children }) {
    return (
        <div className="min-h-screen bg-slate-950 flex flex-col">
            {/* top Navbar */}
            <Navbar />

            {/* Sidebar + main content */}
            <div className="flex flex-1">
                <Sidebar />

            {/* Page content */}
                <main className="flex-1 p-6 text-white">
                    {children}
                </main>
            </div>
        </div>
    )
}

export default Layout    