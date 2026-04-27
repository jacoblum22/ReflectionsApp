/**
 * MVP entry schema — only the fields needed for the core loop:
 * write an entry, talk to the LLM about it.
 *
 * Deferred to post-MVP:
 *   - node_type: only needed when person/event nodes are introduced
 *   - status:    only needed when AI-generated nodes are introduced
 *   - tags:      useful for retrieval, but not required for basic chat
 *   - updated_at / metadata: deferred as noted in design doc
 */
export interface Entry {
  node_id: string       // UUID — auto-generated on save, not shown to user
  title_or_name: string
  created_at: string   // YYYY-MM-DD — defaults to today, user-editable
  body_text: string
}
