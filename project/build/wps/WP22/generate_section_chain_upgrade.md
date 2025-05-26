# 🛠️ Design Note – Upgrading `generate_section_chain` for Policy Alignment

## 🎯 Objective
Enrich section drafts with structured, multi-source evidence:
- 📚 Embedded corpus (queryCorpus)
- 🌐 Live GoC alignment (goc_alignment_search)
- 🧠 User memory (DB retrieval)
- 🔎 General web search (Bing via SerpAPI)

---

## 🔧 Components Impacted

### 1. `generate_section_chain.py`
- 🔹 Add calls to `queryCorpus` and `goc_alignment_search`
- 🔹 Pass outputs into synthesizer as structured sections

### 2. `section_synthesizer.py`
- 🔹 Accept segmented input blocks: `memory`, `corpus_chunks`, `alignment_results`, `web_search`
- 🔹 Build distinct sections in the synthesis prompt for each type

### 3. `drafting_rules.md`
- 🔹 Update LLM instructions: cite sources, reflect alignment, use headers

### 4. FYI – No Change Needed
- ✅ `memory_retrieve.py` (memory pull intact)
- ✅ `web_search.py` (Bing + logging intact)

---

## 🧠 Strategy Chosen: **Supplemental Use of All Inputs**
- Always run `queryCorpus`
- Always run `goc_alignment_search`
- Avoid fallback logic – enrich synthesis by default

---

## ✅ Benefits
| Feature       | Value |
|---------------|-------|
| Evidence Depth | Multiple grounded inputs improve draft strength |
| Policy Relevance | .gc.ca alignment increases approval likelihood |
| Traceability  | Clear input types for debugging and refinement |

---

## 🔜 Next Steps
- Patch `generate_section_chain.py` to call both enrichment tools
- Patch `section_synthesizer.py` to structure prompt accordingly
- Patch `drafting_rules.md` to update guidance for LLM output
