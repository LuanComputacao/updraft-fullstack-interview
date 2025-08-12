# UX Notes (Sally – UX Expert)

## Goals

- Fast perceived performance via streaming
- Keep cognitive load low: summaries appear alongside document
- Preserve editing affordances with TipTap consistency

## UI Placement

- Add a collapsible side panel on the document edit page (right side)
- Panel header: "AI Summary"
- States: idle, generating (spinner + token stream), ready (Save/Update), error

## Interactions

- Generate button pulls current document content and starts stream
- While streaming, show incremental text with typewriter effect and allow cancel
- On finish, enable Save to persist as document summary
- Allow inline editing in TipTap; Update writes back; Delete clears summary

## Empty/Loading/Error

- Empty: explain feature and show Generate CTA
- Loading: subtle progress + estimated time if available
- Error: clear message and retry option; keep partial text if any

## Accessibility

- Keyboard: tab order, buttons focus-visible, ARIA live region for streaming text
- Color contrast meets WCAG AA; avoid relying solely on color for state

## Content Guidelines

- Summary length target: ~10% of doc, 3–7 sentences
- Tone: neutral, concise; avoid hallucinating facts not present in doc
- Provide a "Regenerate" option with quick presets (shorter|longer|key points)
