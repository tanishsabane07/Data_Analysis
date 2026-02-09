import { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function Auth({ user, token, onLogin, onLogout }) {
    const [mode, setMode] = useState('login')
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setSuccess(null)

        try {
            if (mode === 'login') {
                const response = await axios.post(`${API_BASE}/api/auth/login/`, {
                    username,
                    password
                })
                setSuccess('Login successful!')
                onLogin(response.data.user, response.data.token)
                setUsername('')
                setPassword('')
            } else {
                const response = await axios.post(`${API_BASE}/api/auth/register/`, {
                    username,
                    email,
                    password
                })
                setSuccess('Registration successful! You are now logged in.')
                onLogin(response.data.user, response.data.token)
                setUsername('')
                setEmail('')
                setPassword('')
            }
        } catch (err) {
            console.error('Auth error:', err)
            setError(err.response?.data?.error || err.response?.data?.username?.[0] || 'Authentication failed')
        } finally {
            setLoading(false)
        }
    }

    const handleLogout = async () => {
        setLoading(true)
        try {
            await axios.post(`${API_BASE}/api/auth/logout/`, {}, {
                headers: { Authorization: `Token ${token}` }
            })
        } catch (err) {
            // Ignore logout errors
        } finally {
            setLoading(false)
            onLogout()
            setSuccess('Logged out successfully')
        }
    }

    // If user is logged in, show account info
    if (user) {
        return (
            <div className="auth-container">
                <div className="card">
                    <div className="card-header">
                        <h2 className="card-title">👤 Account</h2>
                    </div>

                    {success && <div className="alert alert-success">{success}</div>}

                    <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                        <div style={{
                            width: '80px',
                            height: '80px',
                            borderRadius: '50%',
                            background: 'linear-gradient(135deg, var(--primary-500), var(--accent-purple))',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            margin: '0 auto 1rem',
                            fontSize: '2rem'
                        }}>
                            {user.username?.charAt(0).toUpperCase()}
                        </div>
                        <h3 style={{ marginBottom: '0.5rem' }}>{user.username}</h3>
                        <p style={{ color: 'var(--text-secondary)' }}>{user.email || 'No email provided'}</p>
                    </div>

                    <div style={{
                        padding: '1rem',
                        background: 'var(--bg-secondary)',
                        borderRadius: 'var(--radius-md)',
                        marginBottom: '1.5rem'
                    }}>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                            ✨ Benefits of being logged in:
                        </p>
                        <ul style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', paddingLeft: '1.25rem' }}>
                            <li>Your upload history is saved separately</li>
                            <li>Access your datasets from any device</li>
                            <li>Secure token-based authentication</li>
                        </ul>
                    </div>

                    <button
                        className="btn btn-secondary"
                        onClick={handleLogout}
                        disabled={loading}
                        style={{ width: '100%', justifyContent: 'center' }}
                    >
                        {loading ? '⏳ Logging out...' : '🚪 Logout'}
                    </button>
                </div>
            </div>
        )
    }

    return (
        <div className="auth-container">
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">🔐 {mode === 'login' ? 'Login' : 'Register'}</h2>
                </div>

                {error && <div className="alert alert-error">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter username"
                            required
                        />
                    </div>

                    {mode === 'register' && (
                        <div className="form-group">
                            <label className="form-label">Email (optional)</label>
                            <input
                                type="email"
                                className="form-input"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter email"
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter password"
                            required
                            minLength={mode === 'register' ? 6 : undefined}
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                        style={{ width: '100%', justifyContent: 'center', padding: '1rem' }}
                    >
                        {loading ? '⏳ Please wait...' : mode === 'login' ? '🚀 Login' : '✨ Create Account'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                        {mode === 'login' ? "Don't have an account?" : "Already have an account?"}
                        <button
                            type="button"
                            onClick={() => {
                                setMode(mode === 'login' ? 'register' : 'login')
                                setError(null)
                                setSuccess(null)
                            }}
                            style={{
                                background: 'none',
                                border: 'none',
                                color: 'var(--primary-400)',
                                cursor: 'pointer',
                                marginLeft: '0.5rem',
                                fontWeight: 500
                            }}
                        >
                            {mode === 'login' ? 'Register' : 'Login'}
                        </button>
                    </p>
                </div>

                <div style={{
                    marginTop: '1.5rem',
                    padding: '1rem',
                    background: 'var(--bg-secondary)',
                    borderRadius: 'var(--radius-md)',
                    textAlign: 'center'
                }}>
                    <p style={{ color: 'var(--text-tertiary)', fontSize: '0.8rem' }}>
                        💡 Login is optional. You can use the app without an account,
                        but your history will be shared with other anonymous users.
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Auth
