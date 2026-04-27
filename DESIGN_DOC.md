# ReflectionsApp Design Document (Current)

## 1. Product Summary

ReflectionsApp is a personal diary app centered on writing entries and reflecting on them through conversations with a local LLM.

Core interaction:

- User writes diary entries.
- Entries are stored as Markdown files with metadata and unique keys.
- User can discuss and reflect on entries with a local LLM.
- User can manually create connections between nodes using keys.

Node types currently in scope:

- `entry` (MVP)

Deferred to post-MVP:

- `person`
- `event`

Future direction:

- RAG-based retrieval across nodes and chunks.
- Background AI reflection and AI-generated nodes/connections with human review flow.

## 2. Architecture and Stack

### MVP stack

- React frontend
- FastAPI backend
- Ollama for local model inference

### Planned data and retrieval stack (beyond MVP)

- SQLite for indexed metadata and relationships
- Chroma for vector search (semantic retrieval)

## 3. Source of Truth (Do Now)

System of record:

- Markdown files store full human-readable content.
- SQLite stores indexed metadata and relationships.
- Chroma is a derived cache only.

## 4. Node Model (Do Now)

### MVP entry schema

- `node_id` (UUID, auto-generated)
- `title_or_name`
- `created_at`
- `body_text`

### Full base schema (post-MVP)

When person/event nodes and AI-generated content are introduced, all nodes share:

- `node_id` (UUID)
- `node_type` (`entry`, `person`, `event`, etc.)
- `title_or_name`
- `created_at`
- `updated_at`
- `tags`
- `body_text`
- `status` (`human`, `ai_confirmed`, `ai_unconfirmed`)
- `metadata` (flexible object for type-specific fields)

Examples of type-specific metadata:

- Person: `age`, `birthday`, `relationship`
- Event: `event_date`

## 5. Markdown File Format (Do Now)

Metadata format is YAML frontmatter.

### Entry example

```markdown
---
node_type: entry
node_id: <uuid>
title_or_name: <title>
created_at: <date>
updated_at: <date>
tags: [tag1, tag2, tag3]
status: human
metadata: {}
---

text text text
```

### Person example

```markdown
---
node_type: person
node_id: <uuid>
title_or_name: <name>
created_at: <date>
updated_at: <date>
tags: [tag1, tag2, tag3]
status: human
metadata:
 age: <age>
 birthday: <birthday>
 relationship: <relationship>
---

text text text
```

### Event example

```markdown
---
node_type: event
node_id: <uuid>
title_or_name: <title>
created_at: <date>
updated_at: <date>
tags: [tag1, tag2, tag3]
status: human
metadata:
 event_date: <date>
---

text text text
```

## 6. Connections (Current + Decision)

Current format:

- Pair-based key links in a connections file.
- Example rows: `Key1, Key2`.

Decision:

- Keep the basic pair model for now.
- Defer weight/confidence to later.
- Include `created_by` (human or AI) and timestamps for auditability.

## 7. Retrieval and RAG Roadmap

### MVP

- Chat and reflection with local LLM.
- No full RAG ensemble implementation yet.

### Later

- Ensemble retrieval methods can include:
  - Semantic search
  - Tag search
  - Keyword search
  - Node adjacency via connections
- Reranking/normalization and per-method caps are deferred.
- Retrieval traceability is kept: each retrieved chunk includes source node and retrieval method.

## 8. AI-Generated Content and Review Flow

Three node statuses are part of the long-term model:

- Human-written nodes
- AI-written confirmed nodes
- AI-written unconfirmed nodes

Future behavior:

- Background reflection may create/edit AI nodes or add connections.
- These go to an inbox for review.
- Accept moves into confirmed set.
- Reject deletes from unconfirmed set.
- AI may ask follow-up questions in later conversations.

Governance detail beyond this is deferred.

## 9. Background Agent (Later)

Background agent is not part of MVP.

Current speculation captured:

- Runs only when plugged in/receiving power.
- Could continuously reflect.
- One possible mode is two agents conversing.
- They may initiate searches as needed.
- Potential ping throttling around one per hour.
- Thresholding strategy is still open and may use examples.

## 10. Security, Privacy, and Prompt Injection

Decision for MVP:

- Broad security/privacy work is deferred (single-user local MVP).

Included now:

- Guard against prompt injection from stored notes.

## 11. Performance / Lag Controls (Do Now)

To prevent lag, include caps/limits in the MVP implementation.

## 12. Migration Strategy (Do Now)

Migration/versioning strategy is included from the beginning.

## 13. Decision Log (Do Now vs Later)

Do now:

- Source of truth definition (Markdown + SQLite + Chroma derived)
- Normalized node schema with flexible type-specific metadata
- YAML frontmatter metadata format
- Connection auditability fields (`created_by`, timestamps)
- Performance caps/limits for lag prevention
- Migration strategy from the start
- Prompt-injection protection from stored notes

Later:

- Connection weights/confidence
- Full RAG reranking/score normalization/per-method caps
- Expanded AI governance details
- Background agent implementation
- Broad security/privacy hardening
