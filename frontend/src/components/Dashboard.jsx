import { useState, useEffect } from 'react'
import axios from 'axios'
import { Pie, Bar, Line } from 'react-chartjs-2'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
)

const API_BASE = 'http://localhost:8000'

function Dashboard({ dataset, token }) {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    // Colors for charts
    const chartColors = [
        'rgba(59, 130, 246, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(6, 182, 212, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(34, 197, 94, 0.8)'
    ]

    const borderColors = chartColors.map(c => c.replace('0.8', '1'))

    // Pie chart data - Equipment Type Distribution
    const pieData = {
        labels: Object.keys(dataset.type_distribution || {}),
        datasets: [{
            data: Object.values(dataset.type_distribution || {}),
            backgroundColor: chartColors,
            borderColor: borderColors,
            borderWidth: 2
        }]
    }

    const pieOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#94a3b8',
                    padding: 15,
                    font: { size: 12 }
                }
            },
            title: {
                display: false
            }
        }
    }

    // Bar chart data - Average Values
    const barData = {
        labels: ['Flowrate (L/min)', 'Pressure (bar)', 'Temperature (°C)'],
        datasets: [{
            label: 'Average Values',
            data: [
                dataset.avg_flowrate || 0,
                dataset.avg_pressure || 0,
                dataset.avg_temperature || 0
            ],
            backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)'
            ],
            borderColor: [
                'rgba(59, 130, 246, 1)',
                'rgba(16, 185, 129, 1)',
                'rgba(245, 158, 11, 1)'
            ],
            borderWidth: 2,
            borderRadius: 8
        }]
    }

    const barOptions = {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            y: {
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
                ticks: { color: '#94a3b8' },
                beginAtZero: true
            }
        }
    }

    // Line chart data - Parameter trends across equipment
    const records = dataset.records || []
    const lineData = {
        labels: records.slice(0, 15).map(r => r.equipment_name?.substring(0, 10) || ''),
        datasets: [
            {
                label: 'Flowrate',
                data: records.slice(0, 15).map(r => r.flowrate || 0),
                borderColor: 'rgba(59, 130, 246, 1)',
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                tension: 0.4
            },
            {
                label: 'Pressure',
                data: records.slice(0, 15).map(r => r.pressure || 0),
                borderColor: 'rgba(16, 185, 129, 1)',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                tension: 0.4
            },
            {
                label: 'Temperature',
                data: records.slice(0, 15).map(r => r.temperature || 0),
                borderColor: 'rgba(245, 158, 11, 1)',
                backgroundColor: 'rgba(245, 158, 11, 0.2)',
                tension: 0.4
            }
        ]
    }

    const lineOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#94a3b8',
                    padding: 15
                }
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
                ticks: { color: '#94a3b8', maxRotation: 45 }
            },
            y: {
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
                ticks: { color: '#94a3b8' }
            }
        }
    }

    const handleDownloadPDF = async () => {
        setLoading(true)
        setError(null)
        try {
            const headers = {}
            if (token) {
                headers['Authorization'] = `Token ${token}`
            }

            const response = await axios.get(`${API_BASE}/api/report/${dataset.id}/`, {
                headers,
                responseType: 'blob'
            })

            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', `equipment_report_${dataset.id}.pdf`)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
        } catch (err) {
            setError('Failed to generate PDF report')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            {/* Summary Statistics */}
            <div className="card" style={{ marginBottom: '1.5rem' }}>
                <div className="card-header">
                    <h2 className="card-title">📊 Summary Statistics</h2>
                    <button
                        className="btn btn-success"
                        onClick={handleDownloadPDF}
                        disabled={loading}
                    >
                        {loading ? '⏳ Generating...' : '📄 Download PDF Report'}
                    </button>
                </div>

                {error && <div className="alert alert-error">{error}</div>}

                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-value">{dataset.total_count || 0}</div>
                        <div className="stat-label">Total Equipment</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value green">{dataset.avg_flowrate?.toFixed(1) || 0}</div>
                        <div className="stat-label">Avg Flowrate (L/min)</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value purple">{dataset.avg_pressure?.toFixed(1) || 0}</div>
                        <div className="stat-label">Avg Pressure (bar)</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value orange">{dataset.avg_temperature?.toFixed(1) || 0}</div>
                        <div className="stat-label">Avg Temperature (°C)</div>
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
                <div className="card">
                    <h3 className="chart-title">Equipment Type Distribution</h3>
                    <div className="chart-container" style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Pie data={pieData} options={pieOptions} />
                    </div>
                </div>

                <div className="card">
                    <h3 className="chart-title">Average Parameter Values</h3>
                    <div className="chart-container">
                        <Bar data={barData} options={barOptions} />
                    </div>
                </div>
            </div>

            {/* Line Chart - Full Width */}
            <div className="card" style={{ marginTop: '1.5rem', marginBottom: '1.5rem' }}>
                <h3 className="chart-title">Parameter Trends Across Equipment</h3>
                <div className="chart-container">
                    <Line data={lineData} options={lineOptions} />
                </div>
            </div>

            {/* Data Table */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📋 Equipment Records</h2>
                    <span style={{ color: 'var(--text-secondary)' }}>
                        {records.length} records
                    </span>
                </div>

                <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Equipment Name</th>
                                <th>Type</th>
                                <th>Flowrate (L/min)</th>
                                <th>Pressure (bar)</th>
                                <th>Temperature (°C)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {records.map((record, index) => (
                                <tr key={record.id || index}>
                                    <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>
                                        {record.equipment_name}
                                    </td>
                                    <td>
                                        <span style={{
                                            padding: '0.25rem 0.75rem',
                                            background: 'rgba(59, 130, 246, 0.2)',
                                            borderRadius: '9999px',
                                            fontSize: '0.8rem',
                                            color: 'var(--primary-400)'
                                        }}>
                                            {record.equipment_type}
                                        </span>
                                    </td>
                                    <td>{record.flowrate?.toFixed(1)}</td>
                                    <td>{record.pressure?.toFixed(1)}</td>
                                    <td>{record.temperature?.toFixed(1)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}

export default Dashboard
