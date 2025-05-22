# 🧠 Vector Memory Store – Design Note

## Purpose
To support retrieval-augmented generation (RAG) across user-uploaded and embedded documents, this memory store will house vectorized representations of text chunks. These can be queried to generate, edit, or critique gate-based documentation in PolicyGPT.

## Use Cases
- **loadCorpus** tool stores files or extracted text as vector embeddings.
- **Planner toolchains** retrieve semantically relevant chunks to inform drafting and editing.
- **InputChecker and compose_and_cite** tools validate claims or cite sources using this memory store.

## Storage Design
- We use a vector DB (e.g., Chroma or FAISS, initially local) to store chunked and embedded documents.
- Each chunk is associated with rich metadata:
  - `source_file_id`: ID of original file
  - `chunk_index`: position in file
  - `gate`, `artifact`, `section`, `intent`: when applicable
  - `upload_time`, `session_id`, `user_id`

## Corpus vs. Upload Inputs
- **uploadTextInput / uploadFileInput / uploadLinkInput** write user-generated inputs to PromptLog for context building.
- **loadCorpus** is used when user explicitly uploads larger corpus of background or reference documents intended to inform document creation.

## Deeper Document Generation
“Deeper” here refers to richer contextual grounding and semantic recall:
- Users may upload previous versions of project documents, research reports, strategic plans.
- These are semantically embedded and retrieved using similarity search.
- They enrich the GPT’s ability to make relevant, grounded suggestions.

## Retrieval Usage
- Vector DB is queried by:
  - **Planner Toolchains** when drafting content for a specific gate > artifact > section.
  - **inputChecker** when verifying inputs.
  - **compose_and_cite** when inserting claims or citations into the draft.

## Security & Permissions
- All records will store `session_id` and `user_id` for isolation.
- Future extensions may include document-level access control and TTL (time to live).

## References
- Planning system references this DB via retrieval utils.
- PromptLog can include reference to document IDs used during generation.

## Open Questions
- Standardization of embedding model (OpenAI Embeddings or local)?
- Chunking strategy: semantic vs. fixed size?
- Performance benchmarks at scale?

---

File owner: WP16Pod
To be extended as part of test and tuning phases in coordination with downstream WPs.
