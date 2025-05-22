| Tool                   | Owning WP | Status       | Notes / Pointers                                                                 |
|------------------------|-----------|--------------|----------------------------------------------------------------------------------|
| compose_and_cite       | TBD       | ⏳ Unassigned | Chained logic: search, synth, draft, validate. Recommend splitting WP.          |
| searchKnowledgeBase    | WP4       | 🚫 Deferred  | Needs memory embedding + recall logic. See WP3b, WP9 for context.               |
| externalWebSearch      | WP13      | ⏳ Not started| Planning + citation fallback logic needed.                                       |
| composeDraft           | WP4       | ⏳ Not started| GPT YAML to Markdown generation. Stub exists.                                   |
| validateSection        | WP5       | ⏳ Not started| Markdown schema checker. Pre-validation needed.                                 |
| logReasoningTrace      | WP7       | ⏳ Not started| Trace writer exists. Needs Planner integration.                                 |
| commitSection          | WP6       | ⏳ Not started| Store to DB + Drive. Requires validated section.                                |
| commitDocument         | WP6       | ⏳ Not started| Assembles doc from sections + stores.                                           |
| fetchDocument          | WP6       | ⏳ Not started| Retrieve markdown/doc/pdf.                                                      |
| getTokenUsage          | WP2       | ⏳ Not started| Monitors GPT session. Stats + warnings.                                         |
| translateDocument      | WP10      | ⏳ Not started| Markdown translation tool.                                                      |
| queryAirtable          | WP15      | ⏳ Not started| Needs Airtable API token + lookup logic.                                        |
| parseTranscript        | WP11      | ⏳ Not started| NLP parser from transcript to YAML.                                             |
| loadCorpus             | WP16      | ⏳ Not started| Embeds document into KB. Corpus indexing.                                       |
| doc_feedback_to_task   | WP8       | ⏳ Not started| Converts feedback into planner retry task.                                      |
| diff_and_summarize_sections | WP5  | ⏳ Not started| Compare section versions. Output changelog.                                     |
| submitDocumentFeedback | WP8       | ⏳ Not started| User feedback collector.                                                        |
| summarize_feedback_log | WP8       | ⏳ Not started| Aggregates feedback entries into themes.                                        |
| uploadTextInput        | WP9       | ✅ Complete  | Logs freeform text + YAML + DB. See WP9 tools + schema.                         |
| uploadFileInput        | WP9       | ✅ Complete  | Extracts content from file. YAML + DB logs. See WP9 + text_extractor.py.        |
| uploadLinkInput        | WP9       | ✅ Complete  | Pulls and logs content from URL.                                                |
| createSessionSnapshot  | WP9       | ✅ Complete  | Captures memory snapshot into DB.                                               |