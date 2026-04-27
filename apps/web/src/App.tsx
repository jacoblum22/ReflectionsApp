import { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data: { status: string }) => setStatus(data.status))
      .catch((err: unknown) => setError(String(err)))
  }, [])

  return (
    <div>
      <h1>ReflectionsApp</h1>
      {!status && !error && <p>Checking API…</p>}
      {status && <p>API status: {status}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  )
}

export default App
