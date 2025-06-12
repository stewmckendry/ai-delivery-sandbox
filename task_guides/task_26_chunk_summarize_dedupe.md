# Task 26: Chunking, Summarization, and Deduplication

## 🎯 Goal
Split large content blocks into clean, meaningful segments, summarize if needed, and remove duplicates or overlaps.

## 📂 Target Files
- `app/cleaner.py`

## 📋 Instructions
- Accept list of text blocks or extracted content
- Chunk by:
  - Sentence, heading, or token count
- Deduplicate using:
  - Hashing (exact match)
  - Embedding similarity (optional)
- Summarize long sections (over 1000 tokens) using `summarizer.py`
- Output clean list of non-redundant segments

## 🧪 Test
- Provide overlapping text blocks and validate deduped output
- Check summarization logic with mocked LLM

## ✅ What to Report Back
- Cleaner module
- Summary + dedupe output example
- Test with varied input