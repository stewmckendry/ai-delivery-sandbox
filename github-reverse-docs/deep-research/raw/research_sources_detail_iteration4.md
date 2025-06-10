## Citations

---

### IngestInputChain.py

```python
tool_map = { "text": "uploadTextInput", "file": "uploadFileInput", "link": "uploadLinkInput" }
upload_tool = self.registry.get_tool(tool_map[method])
upload_result = upload_tool.run_tool(inputs, log_usage=False)
```

---

```python
project_profile = self.generate_project_profile(raw_text, metadata, existing)
logger.debug(f"Generated project profile: {project_profile}")
for k, v in project_profile.items():
    logger.debug(f"Generated field {k}: {v} ({type(v)})")
```

---

```python
def generate_project_profile(self, text: str, metadata: dict, existing: dict = None) -> dict:
    schema = """
    project_profile:
      project_id: string
      title: string
      sponsor: string
      project_type: string
      total_budget: number (use null if missing)
      start_date: date (YYYY-MM-DD, use null if missing)
      end_date: date (YYYY-MM-DD, use null if missing)
    """
```

---

```python
log_tool_usage(
    tool_name=tool_map[method],
    input_summary=f"{inputs.get(method) or inputs.get('file_path')} | {tool_map[method]}",
    output_summary=raw_text[:200],
    session_id=metadata.get("session_id"),
    user_id=metadata.get("user_id"),
    metadata=metadata
)
```

---

```python
metadata_project_id = metadata.get("project_id")
if not metadata_project_id:
    logger.error("Input metadata missing required project_id")
    raise ValueError("Input metadata must include project_id")
```

---

```python
def run(self, inputs: dict):
    method = inputs.get("input_method")
    logger.info(f"Running IngestInputChain with method: {method}")
    if method not in ["text", "file", "link"]:
        raise ValueError("input_method must be one of: text, file, link")
```

---

### memory_retrieve.py

```python
logger.info(f"Retrieving entries for artifact={artifact_id}, project_id={project_id}")
query = session.query(PromptLog).filter(
    PromptLog.tool.in_(tool_names),
    PromptLog.project_id == project_id
)
```

---

```python
entries = query.order_by(PromptLog.timestamp.asc()).all()
# Remove entries with duplicate output_summary, keeping the first occurrence
seen_summaries = set()
unique_entries = []
for entry in entries:
    if entry.output_summary not in seen_summaries:
        unique_entries.append(entry)
    seen_summaries.add(entry.output_summary)
entries = unique_entries
```

---

```python
if entry.output_summary not in seen_summaries:
    unique_entries.append(entry)
seen_summaries.add(entry.output_summary)
entries = unique_entries
logger.info(f"Found {len(entries)} entries for artifact={artifact_id}, session_id={session_id}, user_id={user_id}")
return [{
    "input_summary": e.input_summary,
    "output_summary": e.output_summary,
    "full_input_path": e.full_input_path,
    # ...
}]
```

---

### spillover_tracker.md

| Integrate ingestion logs with Planner | WP9 | Planner unaware of ingestion | WP2/WP3a | Unassigned |
| Use PromptLog and SessionSnapshot in doc gen | WP9 | Data present, not yet used downstream | WP2/WP4 | Unassigned |
| Cloud storage of logs (Drive or S3) | WP9 | Currently writes to disk only | WP6 or new infra WP | Unassigned |
| Update `trace_utils.write_trace` for cloud | WP9 | Local path only | WP3c or WP6 | Unassigned |
| Update `createSessionSnapshot` for cloud | WP9 | Local-only logging | WP3c or WP6 | Unassigned |
| Input mode support in session logging | WP16 | Requires metadata tagging | WP3a | Unassigned |
| Mode-aware logic in document assembly | WP16 | Requires mode detection | WP4/WP6 | Unassigned |

---

GitHub  
IngestInputChain.py  
def run(self, inputs: dict): method = inputs.get("input_method") logger.info(f"Running IngestInputChain with method: {method}") if method not in ["text", "file", "link"]: raise ValueError("input_method must be one of: text, file, link")

---

GitHub  
GitHub  
memory.yaml  
- path: project/build/wps/WP17b/WP17b_exit_report.md raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/main/project/build/wps/WP17b/WP17b_exit_report.md file_type: md description: Report detailing the development and implementation of the `generate_section` toolchain for automated document section drafting, including its components, benefits, and technical framework. tags: - toolchain - document_generation - logging

---

GitHub  
GitHub  
section_synthesizer.py  
logger.info(f"[Tool] section_synthesizer user prompt: {user_prompt[:250]}...")

---

GitHub  
GitHub  
finalizeDocument.py  
logger.info("Running finalizeDocument tool") data = parse_obj_as(InputSchema, input_dict) header = f"# {data.title}\n\n**Version:** {data.version} \\\n**Artifact ID:** {data.artifact_id} \\\n**Gate ID:** {data.gate_id} \\\n**Generated On:** {datetime.utcnow().isoformat()}\n\n---\n"

---

GitHub  
GitHub  
formatSection.py  
# Check if section_text starts with a heading (#) if section_text.lstrip().startswith("#"): logger.info(f"Section {data.section_id} starts with a heading, stripping it") # Find the position of the first newline after the heading first_newline = section_text.find('\n') if first_newline != -1: # Strip out the heading (from # to first \n) section_text = section_text[first_newline + 1:].lstrip() else:

---

GitHub  
GitHub  
formatSection.py  
template_text = "<a id=\"{{ section_id }}\"></a>\n## {{ section_title }}\n\n{{ text }}" template = Template(template_text) output = template.render( text=section_text, section_title=data.section_title, section_id=data.section_id ) return OutputSchema(formatted_section=output).dict()

---

GitHub  
GitHub  
mergeSections.py  
def run_tool(self, input_dict: Dict) -> Dict: logger.info("Running mergeSections tool") data = parse_obj_as(InputSchema, input_dict) merged = "\n\n".join(data.sections) return OutputSchema(document_body=merged).dict()

---

GitHub  
GitHub  
finalizeDocument.py  
toc = "## Table of Contents\n" for section in data.sections: title = section.get("title", "") section_id = section.get("section_id", "") toc += f"- [{title}](#{section_id})\n" toc += "\n"

---

GitHub  
GitHub  
storeToDrive.py  
html_content = markdown2.markdown(data.final_markdown) pdf_bytes = HTML(string=html_content).write_pdf()

---

GitHub  
GitHub  
storeToDrive.py  
media = MediaInMemoryUpload(pdf_bytes, mimetype="application/pdf") file_metadata = { "name": filename, "parents": [folder_id], } file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

---

GitHub  
GitHub  
storeToDrive.py  
logger.info("File uploaded successfully with webViewLink: %s", file["webViewLink"]) return OutputSchema(drive_url=file["webViewLink"]).dict()

---

GitHub  
GitHub  
storeToDrive.py  
def _get_or_create_subfolders(self, service, root_id, data): def find_or_create(name, parent): query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents" results = service.files().list(q=query, fields="files(id, name)").execute() files = results.get("files", []) if files: return files[0]["id"] metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]} file = service.files().create(body=metadata, fields="id").execute() return file["id"]

---

GitHub  
GitHub  
storeToDrive.py  
"name": filename, "parents": [folder_id], } file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

---

GitHub  
GitHub  
storeToDrive.py  
} service.permissions().create(fileId=file["id"], body=permission, sendNotificationEmail=False).execute()

---

GitHub  
GitHub  
storeToDrive.py  
for email in SHARE_WITH: permission = { 'type': 'user', 'role': 'reader', 'emailAddress': email } service.permissions().create(fileId=file["id"], body=permission, sendNotificationEmail=False).execute()

---

GitHub  
GitHub  
WP20_design_plan.md  
| File | Purpose | |------|---------| | `storeToDrive.py` | Uploads markdown/PDFs into `/PolicyGPT/<project>/<gate>/<artifact>` folder paths | | `fetchFromDrive.py` | Fetches preview or full file from Drive based on metadata | | `drive_structure.yaml` | Config for folder routing logic | | `test_drive_storage.py` | CLI test for upload + fetch tool | | `test_results.md` | Record of test output | | `WP20_implementation_notes.md` | Design + technical integration notes | | `gpt_user_flow_with_drive.md` | GPT scenario using Drive links |

---

GitHub  
GitHub  
storeToDrive.py  
logger.info("File uploaded successfully with webViewLink: %s", file["webViewLink"]) return OutputSchema(drive_url=file["webViewLink"]).dict()

---

GitHub  
GitHub  
storeToDrive.py  
def _get_or_create_subfolders(self, service, root_id, data): def find_or_create(name, parent): query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents" results = service.files().list(q=query, fields="files(id, name)").execute() files = results.get("files", []) if files: return files[0]["id"] metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]} file = service.files().create(body=metadata, fields="id").execute() return file["id"]

---

GitHub  
GitHub  
WP20_design_plan.md  
Logging + Patching - [ ] Patch `assemble_artifact_chain` to call `storeToDrive` - [ ] Update `DocumentVersionLog` with final Drive URL

---

GitHub  
GitHub  
WP20_design_plan.md  
Journey A – Iterative Drafting - GPT composes section → validator passes →