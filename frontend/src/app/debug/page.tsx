'use client'

import { useEffect, useState } from 'react'

export default function DebugPage() {
  const [apiUrl, setApiUrl] = useState<string>('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Check if we can access the API URL
    const url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    setApiUrl(url)
    
    // Test API connection
    fetch('/api/health')
      .then(res => res.json())
      .then(data => {
        console.log('API Response:', data)
        setError(null)
      })
      .catch(err => {
        console.error('API Error:', err)
        setError(err.message)
      })
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>DecoRoute Debug Page</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <h3>Environment Variables</h3>
        <p><strong>NEXT_PUBLIC_API_URL:</strong> {apiUrl}</p>
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <h3>API Connection Test</h3>
        {error ? (
          <p style={{ color: 'red' }}>❌ Error: {error}</p>
        ) : (
          <p style={{ color: 'green' }}>✅ API connected successfully</p>
        )}
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <h3>Manual API Test</h3>
        <button 
          onClick={() => {
            fetch('/api/health')
              .then(res => res.json())
              .then(data => alert('API Response: ' + JSON.stringify(data)))
              .catch(err => alert('API Error: ' + err.message))
          }}
        >
          Test Health Endpoint
        </button>
      </div>
    </div>
  )
}
