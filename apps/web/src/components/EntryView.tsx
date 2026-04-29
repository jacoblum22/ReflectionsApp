import type { EntryDetail } from '../types/entry'

interface Props {
  entry: EntryDetail
}

export function EntryView({ entry }: Props) {
  return (
    <article className="entry-view">
      <h2>{entry.title_or_name}</h2>
      <p className="entry-view-date">{entry.created_at}</p>
      {/* Render body as plain text; whitespace-pre-wrap preserves line breaks */}
      <div className="entry-view-body">{entry.body_text}</div>
    </article>
  )
}
