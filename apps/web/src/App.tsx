import { useState } from 'react'
import { EntryForm } from './components/EntryForm'
import type { Entry } from './types/entry'
import './App.css'

function App() {
  const [savedId, setSavedId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleSave(entry: Entry) {
    setError(null)
    try {
      const res = await fetch('/api/entries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
      })

      if (!res.ok) {
        // Surface any validation errors from FastAPI
        const detail = await res.text()
        throw new Error(`${res.status}: ${detail}`)
      }

      const data = (await res.json()) as { node_id: string; file: string }
      setSavedId(data.node_id)
    } catch (err: unknown) {
      setError(String(err))
    }
  }

  return (
    <div>
      <h1>New Entry</h1>

      <EntryForm onSave={handleSave} />

      {savedId && (
        <p className="saved-notice">✓ Entry saved — id: {savedId}</p>
      )}
      {error && (
        <p className="error-notice">Error saving entry: {error}</p>
      )}
    </div>
  )
}

export default App
