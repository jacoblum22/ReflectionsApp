import { useEffect, useState } from 'react'
import { EntryForm } from './components/EntryForm'
import { EntryView } from './components/EntryView'
import { Sidebar } from './components/Sidebar'
import type { Entry, EntryDetail, EntrySummary } from './types/entry'
import './App.css'

// The main area shows either the new-entry form or a selected entry.
type View = 'new' | 'reading'

function App() {
  const [view, setView] = useState<View>('new')
  const [entries, setEntries] = useState<EntrySummary[]>([])
  const [selectedEntry, setSelectedEntry] = useState<EntryDetail | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Load the sidebar list once on mount.
  useEffect(() => {
    fetchEntries()
  }, [])

  async function fetchEntries() {
    try {
      const res = await fetch('/api/entries')
      const data = (await res.json()) as EntrySummary[]
      setEntries(data)
    } catch (err: unknown) {
      setError(String(err))
    }
  }

  async function handleSelectEntry(id: string) {
    setError(null)
    try {
      const res = await fetch(`/api/entries/${id}`)
      if (!res.ok) throw new Error(`${res.status}`)
      const data = (await res.json()) as EntryDetail
      setSelectedEntry(data)
      setSelectedId(id)
      setView('reading')
    } catch (err: unknown) {
      setError(String(err))
    }
  }

  async function handleSave(entry: Entry) {
    setError(null)
    try {
      const res = await fetch('/api/entries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
      })
      if (!res.ok) {
        const detail = await res.text()
        throw new Error(`${res.status}: ${detail}`)
      }
      // Refresh the sidebar so the new entry appears immediately.
      await fetchEntries()
    } catch (err: unknown) {
      setError(String(err))
    }
  }

  return (
    <div className="layout">
      <Sidebar
        entries={entries}
        selectedId={selectedId}
        onSelect={handleSelectEntry}
        onNew={() => { setView('new'); setSelectedId(null) }}
      />

      <main className="main-area">
        {error && <p className="error-notice">{error}</p>}

        {view === 'new' && <EntryForm onSave={handleSave} />}

        {view === 'reading' && selectedEntry && (
          <EntryView entry={selectedEntry} />
        )}
      </main>
    </div>
  )
}

export default App
