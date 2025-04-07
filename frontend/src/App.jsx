import { useState } from 'react'
import axios from 'axios'
import { ThemeProvider } from './components/theme-provider'
import { ThemeToggle } from './components/ui/theme-toggle'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await axios.post('http://localhost:5000/predict', { url })
      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
    setLoading(false)
  }

  const ResultRow = ({ label, value }) => (
    <div className="grid grid-cols-[200px_1fr] gap-4 py-2 border-b border-gray-100 dark:border-gray-800">
      <div className="text-gray-500 dark:text-gray-400">{label}</div>
      <div className="text-gray-900 dark:text-gray-100">{value}</div>
    </div>
  )

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-transparent transition-colors duration-150">
        <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Website Scanner</h1>
            <ThemeToggle />
          </div>
          
          <form onSubmit={handleSubmit} className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-lg shadow-sm p-4 mb-6 flex gap-4 border border-gray-200 dark:border-gray-800">
            <input
              type="text"
              placeholder="Enter URL to scan"
              required
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 px-4 py-2 rounded-md border border-gray-200 dark:border-gray-700 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
            />
            <button 
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Scanning...' : 'Scan Website'}
            </button>
          </form>

          {loading && (
            <div className="flex justify-center my-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}

          {result && !loading && (
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-lg shadow-sm p-6 border border-gray-200 dark:border-gray-800">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Report Summary</h2>
              
              <div className="space-y-2">
                <ResultRow label="Website Address" value={result.website_address} />
                <ResultRow label="Last Analysis" value={result.last_analysis} />
                <ResultRow 
                  label="Detection Status" 
                  value={
                    <span className={result.detection_counts === 'Safe' ? 'text-green-600 dark:text-green-400 font-medium' : 'text-red-600 dark:text-red-400 font-medium'}>
                      {result.detection_counts} ({result.confidence})
                    </span>
                  } 
                />
                <ResultRow label="Domain Registration" value={result.domain_registration} />
                <ResultRow 
                  label="Domain Information" 
                  value={
                    <div className="space-y-1">
                      <div>Registrar: {result.domain_information.registrar}</div>
                      <div>WHOIS Server: {result.domain_information.whois_server}</div>
                      <div>Status: {result.domain_information.status}</div>
                    </div>
                  }
                />
                <ResultRow label="IP Address" value={result.ip_address} />
                <ResultRow label="Server Location" value={result.server_location} />
                <ResultRow label="City" value={result.city} />
                <ResultRow label="Region" value={result.region} />
              </div>
            </div>
          )}
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App
