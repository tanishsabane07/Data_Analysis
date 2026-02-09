import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import CSVUpload from './components/CSVUpload'
import Dashboard from './components/Dashboard'
import History from './components/History'
import Auth from './components/Auth'

function App() {
    const [activeTab, setActiveTab] = useState('upload')
    const [currentDataset, setCurrentDataset] = useState(null)
    const [user, setUser] = useState(null)
    const [token, setToken] = useState(localStorage.getItem('token') || null)
    const navigate = useNavigate()

    useEffect(() => {
        const savedToken = localStorage.getItem('token')
        const savedUser = localStorage.getItem('user')
        if (savedToken && savedUser) {
            setToken(savedToken)
            setUser(JSON.parse(savedUser))
        }
    }, [])

    const handleLogin = (userData, authToken) => {
        setUser(userData)
        setToken(authToken)
        localStorage.setItem('token', authToken)
        localStorage.setItem('user', JSON.stringify(userData))
    }

    const handleLogout = () => {
        setUser(null)
        setToken(null)
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    const handleUploadSuccess = (dataset) => {
        setCurrentDataset(dataset)
        setActiveTab('dashboard')
    }

    const handleSelectDataset = (dataset) => {
        setCurrentDataset(dataset)
        setActiveTab('dashboard')
    }

    return (
        <div className="app-container">
            <header className="header">
                <h1>⚗️ Chemical Equipment Visualizer</h1>
                <p>Analyze and visualize your chemical equipment parameters with ease</p>
                {user && (
                    <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Welcome, {user.username}!</span>
                        <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
                    </div>
                )}
            </header>

            <nav className="nav-tabs">
                <button
                    className={`nav-tab ${activeTab === 'upload' ? 'active' : ''}`}
                    onClick={() => setActiveTab('upload')}
                >
                    📤 Upload
                </button>
                <button
                    className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveTab('dashboard')}
                    disabled={!currentDataset}
                >
                    📊 Dashboard
                </button>
                <button
                    className={`nav-tab ${activeTab === 'history' ? 'active' : ''}`}
                    onClick={() => setActiveTab('history')}
                >
                    📁 History
                </button>
                <button
                    className={`nav-tab ${activeTab === 'auth' ? 'active' : ''}`}
                    onClick={() => setActiveTab('auth')}
                >
                    🔐 {user ? 'Account' : 'Login'}
                </button>
            </nav>

            <main>
                {activeTab === 'upload' && (
                    <CSVUpload token={token} onUploadSuccess={handleUploadSuccess} />
                )}
                {activeTab === 'dashboard' && currentDataset && (
                    <Dashboard dataset={currentDataset} token={token} />
                )}
                {activeTab === 'dashboard' && !currentDataset && (
                    <div className="card">
                        <div className="empty-state">
                            <div className="empty-state-icon">📊</div>
                            <p>No dataset selected. Upload a CSV file or select from history.</p>
                        </div>
                    </div>
                )}
                {activeTab === 'history' && (
                    <History token={token} onSelectDataset={handleSelectDataset} />
                )}
                {activeTab === 'auth' && (
                    <Auth user={user} token={token} onLogin={handleLogin} onLogout={handleLogout} />
                )}
            </main>
        </div>
    )
}

export default App
