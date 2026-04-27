import { useState } from 'react'
import type { Entry } from '../types/entry'

interface Props {
  onSave: (entry: Entry) => void
}

/** Returns today's date as a YYYY-MM-DD string, which is what <input type="date"> expects. */
function todayISO(): string {
  return new Date().toISOString().split('T')[0]
}

export function EntryForm({ onSave }: Props) {
  // Each field is a piece of React state — this is a "controlled form".
  // React owns the values; the DOM just reflects them.
  const [title, setTitle] = useState('')
  const [date, setDate] = useState(todayISO)
  const [body, setBody] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    // node_id is the only field the user never sees — generated automatically.
    const entry: Entry = {
      node_id: crypto.randomUUID(),  // built into modern browsers — no library needed
      title_or_name: title,
      created_at: date,
      body_text: body,
    }

    onSave(entry)

    // Reset the form so it's ready for the next entry.
    setTitle('')
    setDate(todayISO())
    setBody('')
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="field">
        <label htmlFor="title">Title</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="date">Date</label>
        {/* type="date" gives a native date picker and always returns YYYY-MM-DD */}
        <input
          id="date"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>

      <div className="field">
        <label htmlFor="body">Entry</label>
        <textarea
          id="body"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={12}
          required
        />
      </div>

      <button type="submit">Save Entry</button>
    </form>
  )
}
