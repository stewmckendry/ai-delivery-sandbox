## 🔁 WP27 Retrospective – Iteration 4

### ✅ What Went Well
- Full user journey is now covered end-to-end (kickoff → finalization)
- Redis integration made edits fast, live, and modular
- Added structured research logging for both GPT-led and backend-led paths
- LLM prompts + YAML template use kept consistency high
- Test coverage and modular logging enabled confident iteration

### 🧩 What We Built
- Section review & feedback flow
- Redis-persisted edits + chunked drafts
- Input generator to bootstrap UX
- Enhanced `loadCorpus` with HTML parsing + LLM assist
- Research logging (`record_research`) with citation and metadata

### 😓 Challenges
- PromptLog schema unification took iteration to align across tools
- HTML parsing from unpredictable pages introduced noise—LLM step helped
- Clarifying role of front-end ChatGPT vs. backend API GPT was key

### 📘 Lessons Learned
- LLMs are great at *structuring* messy input—let them help with cleaning!
- Tools should log to PromptLog consistently with label patterns (e.g. `global_context`)
- Break research and context steps into small, composable tools
- Use Redis for temporary user-edit workflows; DB for persistent outputs

### 📈 What’s Next
- Custom GPT onboarding + configuration
- Testing end-to-end in ChatGPT UX
- Enhancing review workflows for multi-stakeholder flows

Great iteration! Let’s test it and take it live 🚀