import { useEffect, useRef, useState } from 'react'
import type { ChatMessage } from '../types/entry'

// The model is hardcoded for MVP — a picker can be added later via GET /chat/models.
const MODEL = 'qwen2.5:7b'

interface Props {
  entryId: string
}

export function ChatPanel({ entryId }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  // Reset the conversation when the user opens a different entry.
  useEffect(() => {
    setMessages([])
    setInput('')
    setError(null)
  }, [entryId])

  // Scroll to the bottom after each new message.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(e: React.FormEvent) {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: ChatMessage = { role: 'user', content: input.trim() }
    const nextMessages = [...messages, userMessage]

    setMessages(nextMessages)
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          entry_id: entryId,
          model: MODEL,
          messages: nextMessages,
        }),
      })

      if (!res.ok) {
        const detail = await res.text()
        throw new Error(`${res.status}: ${detail}`)
      }

      const reply = (await res.json()) as ChatMessage
      setMessages((prev) => [...prev, reply])
    } catch (err: unknown) {
      setError(String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <aside className="chat-panel">
      <h2 className="chat-heading">Reflect</h2>

      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="chat-empty">Ask anything about this entry.</p>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message chat-message--${msg.role}`}>
            <span className="chat-role">{msg.role === 'user' ? 'You' : 'AI'}</span>
            <p className="chat-content">{msg.content}</p>
          </div>
        ))}
        {loading && (
          <div className="chat-message chat-message--assistant">
            <span className="chat-role">AI</span>
            <p className="chat-content chat-thinking">Thinking…</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {error && <p className="error-notice">{error}</p>}

      <form className="chat-form" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message…"
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </aside>
  )
}
