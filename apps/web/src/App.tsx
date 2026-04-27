import { useState } from 'react'
import { EntryForm } from './components/EntryForm'
import type { Entry } from './types/entry'
import './App.css'

function App() {
  // lastSaved holds the most recently saved Entry so we can show it as a preview.
  // null means nothing has been saved yet this session.
  const [lastSaved, setLastSaved] = useState<Entry | null>(null)

  return (
    <div>
      <h1>New Entry</h1>

      {/* onSave receives the completed Entry object from the form */}
      <EntryForm onSave={setLastSaved} />

      {lastSaved && (
        <div className="saved-preview">
          <h2>Saved — would send to backend:</h2>
          {/* JSON.stringify with indent=2 makes the structure readable */}
          <pre>{JSON.stringify(lastSaved, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App
