# Retrospective Tracker
...existing entries...

## WP14 – External Source Integration

### ✅ What Went Well
- Successfully wrapped external web search using LLM-guarded retrieval
- Integration with planner and GPT manifest was smooth
- Tool supports parameter validation and OpenAPI traceability

### 🤯 Challenges
- Managing risk of over-fetch or hallucinated citations
- Integrating fallback behavior when no results returned

### 💡 Lessons & Recommendations
- Fallback plan is essential when search fails
- Limit queries to reduce token and API overhead
- Use a validation hook to ensure trusted sources only