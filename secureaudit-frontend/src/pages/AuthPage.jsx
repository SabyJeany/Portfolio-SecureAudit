import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import LoginForm from '../components/LoginForm'
import RegisterForm from '../components/RegisterForm'
import { useAuth } from '../context/AuthContext'

function AuthPage() {
  const [mode, setMode] = useState('login')
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-emerald-400">SECUREAUDIT</h1>
        <p className="text-slate-400 text-sm mt-1">Web security audit platform</p>
      </div>

      {mode === 'login' ? <LoginForm /> : <RegisterForm />}

      <p className="text-slate-400 text-sm mt-6">
        {mode === 'login' ? (
          <>
            Don't have an account?{' '}
            <button
              onClick={() => setMode('register')}
              className="text-emerald-400 hover:underline"
            >
              Sign up
            </button>
          </>
        ) : (
          <>
            Already have an account?{' '}
            <button
              onClick={() => setMode('login')}
              className="text-emerald-400 hover:underline"
            >
              Log in
            </button>
          </>
        )}
      </p>
    </div>
  )
}

export default AuthPage