# WP16 – Input Prompt UX Layer

## ✅ Core Build Tasks

- [x] T1a – Design prompt schema for inputs (section-by-section structure)
- [x] T1b – Build inputPromptGenerator tool (guided UX flow)
- [x] T1c – Add metadata capture in upload tools (mode, gate, artifact, section, intent)
- [x] T2 – Build inputChecker tool to validate user inputs against reference
- [x] T2b – Add Phase 1 evaluation logic (exact match, rule-based)
- [x] T3a – Design vector memory store and deploy strategy
- [x] T3b – Commit vector DB deploy guide and local setup
- [ ] T3c – Build `loadCorpus` tool for loading and embedding documents
- [ ] T3d – Migrate vector DB to cloud (post-PoC) and update deploy guide
- [ ] T4 – Generate UX messages, tool metadata, and starter messages for GPT
- [ ] T5 – Commit and push tool catalog updates, prompt schema reference, and integration notes
- [ ] T6 – Final test run and snapshot export of a sample session
- [ ] T7 – Design GPT Review UX Interface (Input Summary + Confirm to Draft)
- [ ] T8 – Completion note and lead pod update

## 🧩 Patches + Extensions
- [x] Patch upload tools (TextInput, LinkInput, FileInput) to accept and log metadata
- [x] Add support for metadata in structured_input_ingestor and memory_sync
- [x] Patch PromptLog to store metadata blob in `full_input_path` (P5)
- [ ] Add test coverage for ingestion + logging behavior (P6)

## 📣 CR Scope Additions (Handled in T1c)
- Strategy to capture input mode using GPT conversation and memory
- Documentation for GPT config team to implement starter messages + system prompt
- Spillover coordination flagged to Pod Lead

## 🆕 New Deliverable (Handled in T7)
- GPT review interface spec to preview user input before draft generation, per `dense_artifact_generation.md`