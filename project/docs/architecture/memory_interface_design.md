## 💾 MemoryManager Architecture – Dual Backend (Airtable + Notion)

### 🔄 Unified Interface
```python
# memory_manager.py
class MemoryManager:
    def __init__(self, use_airtable=True, use_notion=True):
        self.airtable = AirtableClient() if use_airtable else None
        self.notion = NotionClient() if use_notion else None

    def save_reflection(self, session_id, career_id, prompt_id, text):
        if self.airtable:
            self.airtable.save(session_id, career_id, prompt_id, text)
        if self.notion:
            self.notion.create_journal_entry(session_id, career_id, text)
```

### 📄 AirtableClient
```python
# airtable_client.py
class AirtableClient:
    def save(self, session_id, career_id, prompt_id, text):
        # Use Airtable API to log structured record
        pass
```

### 📄 NotionClient
```python
# notion_client.py
class NotionClient:
    def create_journal_entry(self, session_id, career_id, text):
        # Create a rich page with title, body, tags
        pass
```

### 🔍 Summary
- **Airtable** = tabular memory (structured tracking)
- **Notion** = narrative memory (user journey, shareable)
- Controlled opt-in logic
- Modular, extensible, private by design