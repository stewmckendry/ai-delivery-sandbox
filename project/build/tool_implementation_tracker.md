| Tool ID | Description | Owning WP(s) | Status | Notes |
|---------|-------------|--------------|--------|-------|
| compose_and_cite | Orchestrates evidence search → synthesis → draft → validate | WP4, WP5, WP6 | Planned | Tool wrapper defined in WP3b. Core logic pending. |
| searchKnowledgeBase | Retrieves semantic matches from embedded documents | WP4 | Planned | Tied to memory index. |
| externalWebSearch | Pulls evidence from trusted web sources | WP13 | Planned | External integration. |
| composeDraft | Generates structured markdown from YAML + evidence | WP4 | Planned | For structured draft generation. |
| validateSection | Validates required fields and logic structure | WP5 | Planned | Quality and rules compliance. |
| logReasoningTrace | Stores reasoning trace for each toolchain run | WP7 | Planned | Logs rationale per run. |
| commitSection | Saves validated section to Drive and DB | WP6 | Planned | Integrates storage and routing. |
| commitDocument | Assembles and stores full artifact | WP6 | Planned | Finalization stage. |
| fetchDocument | Retrieves section or full document | WP6 | Planned | For review + edits. |
| getTokenUsage | Tracks GPT session size and overflow risk | WP2 | Planned | Monitoring and diagnostics. |
| translateDocument | Converts document language (EN ⇆ FR) | WP10 | Planned | EN/FR translation logic. |
| queryAirtable | Looks up structured reference mappings | WP15 | Planned | Structured data lookup. |
| parseTranscript | Converts transcripts to YAML insights | WP11 | Planned | NLP and extraction layer. |
| loadCorpus | Embeds and indexes documents into KB | WP16 | Planned | Corpus ingestion and sync. |
| doc_feedback_to_task | Converts feedback into new planner tasks | WP8 | Planned | Feedback → planner integration. |
| diff_and_summarize_sections | Computes section diffs and summarizes changes | WP5 | Planned | Change analysis + QA. |
| submitDocumentFeedback | Captures user feedback on drafts | WP8 | Planned | For human-in-loop input. |
| summarize_feedback_log | Synthesizes feedback entries into summary | WP8 | Planned | Feedback digest + trends. |