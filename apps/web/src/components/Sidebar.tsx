import type { EntrySummary } from '../types/entry'

interface Props {
  entries: EntrySummary[]
  selectedId: string | null
  onSelect: (id: string) => void
  onNew: () => void
}

export function Sidebar({ entries, selectedId, onSelect, onNew }: Props) {
  return (
    <nav className="sidebar">
      <button className="new-button" onClick={onNew}>
        + New
      </button>

      <ul className="entry-list">
        {entries.map((entry) => (
          <li
            key={entry.node_id}
            className={`entry-item ${entry.node_id === selectedId ? 'selected' : ''}`}
            onClick={() => onSelect(entry.node_id)}
          >
            <span className="entry-title">{entry.title_or_name}</span>
            <span className="entry-date">{entry.created_at}</span>
          </li>
        ))}
        {entries.length === 0 && (
          <li className="no-entries">No entries yet</li>
        )}
      </ul>
    </nav>
  )
}
