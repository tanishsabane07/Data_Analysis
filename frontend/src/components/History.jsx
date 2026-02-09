import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function History({ token, onSelectDataset }) {
    const [datasets, setDatasets] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchHistory()
    }, [token])

    const fetchHistory = async () => {
        setLoading(true)
        setError(null)
        try {
            const headers = {}
            if (token) {
                headers['Authorization'] = `Token ${token}`
            }

            const response = await axios.get(`${API_BASE}/api/history/`, { headers })
            setDatasets(response.data)
        } catch (err) {
            setError('Failed to load history')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleSelectDataset = async (datasetId) => {
        try {
            const headers = {}
            if (token) {
                headers['Authorization'] = `Token ${token}`
            }

            const response = await axios.get(`${API_BASE}/api/data/${datasetId}/`, { headers })
            onSelectDataset(response.data)
        } catch (err) {
            setError('Failed to load dataset')
            console.error(err)
        }
    }

    const handleDownloadPDF = async (e, datasetId) => {
        e.stopPropagation()
        try {
            const headers = {}
            if (token) {
                headers['Authorization'] = `Token ${token}`
            }

            const response = await axios.get(`${API_BASE}/api/report/${datasetId}/`, {
                headers,
                responseType: 'blob'
            })

            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', `equipment_report_${datasetId}.pdf`)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
        } catch (err) {
            console.error('PDF download failed:', err)
        }
    }

    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Loading history...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📁 Upload History</h2>
                <button className="btn btn-secondary" onClick={fetchHistory}>
                    🔄 Refresh
                </button>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            {datasets.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">📂</div>
                    <p>No uploads yet. Upload a CSV file to get started!</p>
                </div>
            ) : (
                <div className="history-list">
                    {datasets.map((dataset, index) => (
                        <div
                            key={dataset.id}
                            className="history-item"
                            onClick={() => handleSelectDataset(dataset.id)}
                        >
                            <div className="history-info">
                                <h3>
                                    {index === 0 && '⭐ '}{dataset.filename}
                                </h3>
                                <p>
                                    Uploaded: {formatDate(dataset.uploaded_at)} •
                                    {dataset.total_count} equipment records
                                </p>
                                <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                    {Object.entries(dataset.type_distribution || {}).map(([type, count]) => (
                                        <span
                                            key={type}
                                            style={{
                                                padding: '0.2rem 0.6rem',
                                                background: 'rgba(139, 92, 246, 0.2)',
                                                borderRadius: '9999px',
                                                fontSize: '0.75rem',
                                                color: 'var(--accent-purple)'
                                            }}
                                        >
                                            {type}: {count}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            <div className="history-meta">
                                <div className="history-badge">
                                    Avg Flow: {dataset.avg_flowrate?.toFixed(1)}
                                </div>
                                <button
                                    className="btn btn-success"
                                    onClick={(e) => handleDownloadPDF(e, dataset.id)}
                                    style={{ padding: '0.5rem 1rem' }}
                                >
                                    📄 PDF
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div style={{
                marginTop: '1.5rem',
                padding: '1rem',
                background: 'var(--bg-secondary)',
                borderRadius: 'var(--radius-md)',
                textAlign: 'center'
            }}>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    💡 The system keeps the last 5 uploaded datasets. Click on any dataset to view its dashboard.
                </p>
            </div>
        </div>
    )
}

export default History
