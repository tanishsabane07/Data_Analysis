import { useState, useRef } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function CSVUpload({ token, onUploadSuccess }) {
    const [file, setFile] = useState(null)
    const [dragover, setDragover] = useState(false)
    const [uploading, setUploading] = useState(false)
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)
    const fileInputRef = useRef(null)

    const handleDragOver = (e) => {
        e.preventDefault()
        setDragover(true)
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setDragover(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setDragover(false)
        const droppedFile = e.dataTransfer.files[0]
        if (droppedFile && droppedFile.name.endsWith('.csv')) {
            setFile(droppedFile)
            setError(null)
        } else {
            setError('Please drop a valid CSV file')
        }
    }

    const handleFileSelect = (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile && selectedFile.name.endsWith('.csv')) {
            setFile(selectedFile)
            setError(null)
        } else {
            setError('Please select a valid CSV file')
        }
    }

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file first')
            return
        }

        setUploading(true)
        setError(null)
        setSuccess(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const headers = {}
            if (token) {
                headers['Authorization'] = `Token ${token}`
            }

            const response = await axios.post(`${API_BASE}/api/upload/`, formData, {
                headers: {
                    ...headers,
                    'Content-Type': 'multipart/form-data'
                }
            })

            setSuccess(`Successfully uploaded! Found ${response.data.total_count} equipment records.`)
            setFile(null)
            if (fileInputRef.current) {
                fileInputRef.current.value = ''
            }

            // Notify parent component
            if (onUploadSuccess) {
                onUploadSuccess(response.data)
            }
        } catch (err) {
            console.error('Upload error:', err)
            setError(err.response?.data?.error || 'Failed to upload file. Please try again.')
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📤 Upload CSV File</h2>
            </div>

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <div
                className={`upload-zone ${dragover ? 'dragover' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <div className="upload-icon">📁</div>
                {file ? (
                    <>
                        <p className="upload-text">Selected: <strong>{file.name}</strong></p>
                        <p className="upload-hint">Size: {(file.size / 1024).toFixed(2)} KB</p>
                    </>
                ) : (
                    <>
                        <p className="upload-text">Drag and drop your CSV file here</p>
                        <p className="upload-hint">or click to browse files</p>
                    </>
                )}

                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    accept=".csv"
                    style={{ display: 'none' }}
                />
            </div>

            <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
                <button
                    className="btn btn-primary"
                    onClick={handleUpload}
                    disabled={!file || uploading}
                    style={{ padding: '1rem 2rem', fontSize: '1rem' }}
                >
                    {uploading ? (
                        <>
                            <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '0.5rem' }}></span>
                            Uploading...
                        </>
                    ) : (
                        '🚀 Upload & Analyze'
                    )}
                </button>
            </div>

            <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)' }}>
                <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>📋 Expected CSV Format</h4>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Your CSV file should contain the following columns:
                </p>
                <code style={{
                    display: 'block',
                    marginTop: '0.5rem',
                    padding: '0.75rem',
                    background: 'var(--bg-tertiary)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.875rem',
                    color: 'var(--accent-cyan)'
                }}>
                    Equipment Name, Type, Flowrate, Pressure, Temperature
                </code>
            </div>
        </div>
    )
}

export default CSVUpload
