| Tool                   | Owning WP | Status       | Notes / Pointers                                                                 |
|------------------------|-----------|--------------|----------------------------------------------------------------------------------|
| compose_and_cite       | WP17b     | Deprecated| Replaced by generate_section toolchain                                          |
| searchKnowledgeBase    | WP4       | 🚫 Deferred  | Needs memory embedding + recall logic. See WP3b, WP9 for context.               |
| externalWebSearch      | WP13      | ⏳ Not started| Planning + citation fallback logic needed.                                       |
| composeDraft           | WP4       | Deprecated   | Replaced by generate_section toolchain exists.                                   |
| validateSection        | WP5       | ⏳ Not started| Markdown schema checker. Pre-validation needed.                                 |
| logReasoningTrace      | WP7       | ⏳ Not started| Trace writer exists. Needs Planner integration.                                 |
| commitSection          | WP6       | ⏳ Not started| Store to DB + Drive. Requires validated section.                                |
| commitDocument         | WP6       | ⏳ Not started| Assembles doc from sections + stores.                                           |
| fetchDocument          | WP6       | ⏳ Not started| Retrieve markdown/doc/pdf.                                                      |
| getTokenUsage          | WP2       | ⏳ Not started| Monitors GPT session. Stats + warnings.                                         |
| translateDocument      | WP10      | ⏳ Not started| Markdown translation tool.                                                      |
| queryAirtable          | WP15      | ⏳ Not started| Needs Airtable API token + lookup logic.                                        |
| parseTranscript        | WP11      | ⏳ Not started| NLP parser from transcript to YAML.                                             |
| loadCorpus             | WP16      | ✅ Complete  | Embeds document into KB. Corpus indexing.                                       |
| doc_feedback_to_task   | WP8       | ⏳ Not started| Converts feedback into planner retry task.                                      |
| diff_and_summarize_sections | WP5  | ⏳ Not started| Compare section versions. Output changelog.                                     |
| submitDocumentFeedback | WP8       | ⏳ Not started| User feedback collector.                                                        |
| summarize_feedback_log | WP8       | ⏳ Not started| Aggregates feedback entries into themes.                                        |
| uploadTextInput        | WP9       | ✅ Complete  | Logs freeform text + YAML + DB. See WP9 tools + schema.                         |
| uploadFileInput        | WP9       | ✅ Complete  | Extracts content from file. YAML + DB logs. See WP9 + text_extractor.py.        |
| uploadLinkInput        | WP9       | ✅ Complete  | Pulls and logs content from URL.                                                |
| createSessionSnapshot  | WP9       | ✅ Complete  | Captures memory snapshot into DB.                                               |
| inputPromptGenerator   | WP16      | ✅ Complete  | Generates prompts based on gate + artifact context. See WP16 schema.            |
| inputChecker           | WP16      | ✅ Complete  | Validates prompt inputs for completeness and clarity. See WP16 test plan.       |
| assembleDraft          | WP18      | ✅ Complete  | Combines `ArtifactSection` into full doc. Validates structure.                  |
| commitArtifact         | WP18      | ✅ Complete  | Finalize and log full draft.                                                    |
| storeToDrive           | WP20      | ⏳ Not started| Uploads artifacts to Google Drive under structured folders                      |
| fetchFromDrive         | WP20      | ⏳ Not started| Retrieve Drive documents for review/feedback                                    |
| queryCorpus            | WP21      | ⏳ Not started| Search Chroma vector DB for relevant snippets                                   |
| showProfile            | WP7       | ⏳ Not started| Inspect current project profile (dynamic + persisted)                           |
| project_profile_updater | WP7      | ⏳ Not started| Dynamically update ProjectProfile in session and DB                             |
| prepare_drafting_context | TBD     | ⏳ Not started| Gathers inputs for drafting including PromptLog, KB, and project profile        |
| propose_draft_plan     | TBD       | ⏳ Not started| Generates YAML-based planner task trace per section                             |
| execute_draft_phase    | TBD       | ⏳ Not started| Executes one phase of the draft plan and logs output                            |
| validate_and_commit    | TBD       | ⏳ Not started| Validates and stores the final section content                                  |
| memory_retrieve        | WP17b     | ✅ Complete  | Retrieves relevant memory snippets from PromptLog for use in drafting.          |
| section_synthesizer    | WP17b     | ✅ Complete  | Uses memory and context to generate structured draft content.                   |
| section_refiner        | WP17b     | ✅ Complete  | Refines raw draft using LLM for clarity and tone.                               |
| generate_section       | WP17b     | ✅ Complete  | Planner-registered toolchain combining retrieve → synthesize → refine.         |