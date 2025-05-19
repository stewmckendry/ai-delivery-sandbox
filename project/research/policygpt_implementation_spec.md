# PolicyGPT Implementation Specification

## Custom GPT Configuration

### Prompt Engineering for Long-Form Output

The assistant (“PolicyGPT”) should be given a clear system prompt to adopt the voice and style of a Government project manager writing formal gate artifacts. For example, instruct it:

> “You are PolicyGPT, a government project specialist. Produce complete, detailed documents (20+ pages) for each gate, using formal language (Decision, Evidence, Criteria, Governance, etc.) and bullet lists where appropriate.”

To avoid summary-style replies, the prompt should emphasize full-length sections (e.g. “Write at least 3 paragraphs per section, not bullet summaries”). Use few-shot examples (e.g. excerpts from the Treasury Board Guide) to illustrate tone and structure. For instance, the official Gating Plan template uses labeled sections:

- “Decision to be taken”
- “Evidence: … such as investment proposal or concept case”
- “Criteria: … Is the business problem worth pursuing?”

We can paste a snippet like this into the instructions so PolicyGPT mimics the authoritative style (formal headings, complete sentences, official terminology).

### Hierarchical Outline and Chunking

To manage depth and ensure coverage, prompts should be multi-step. First, instruct the GPT to generate a detailed outline or table of contents covering all required sections and subsections (e.g. Executive Summary, Scope, Risk Assessment, Gate Decision, etc.). Then instruct it to expand one section at a time. For example:

1. **Step 1**: List all sections and subsections of the project gating plan.
2. **Step 2**: For section 1 (Background), write the full section content.

This hierarchical approach helps the model plan before writing. Each section (or group of subsections) can be generated in a separate turn and committed via the tool before moving on. If the output becomes too large, the designer can instruct GPT to wait for a “Continue” prompt or to explicitly write up to a logical break (e.g. “End this section with a transition to the next topic”). The custom GPT tools will help by breaking a document into chunks (sections) for committing.

### Knowledge Files for Reference

Attach relevant reference documents as knowledge files in the GPT builder (up to 20 files). These might include the Treasury Board Guide to Project Gating, sample gate plans, or past artifacts (business cases, charters, etc.). Using knowledge files ensures the GPT can draw on official guidance when writing artifacts. 

In the instruction set, explicitly tell the model to use these files for answers, e.g.:

- “Refer to GuideToProjectGating.pdf when describing gate criteria.”
- “Consult the attached Gating Guide to ensure your content aligns with official language and criteria.”

Because the guide is stable policy content, it is a perfect fit: “Knowledge is best for contexts that change infrequently (policy documents, guidelines, etc.).” We can also include a project-specific knowledge file (e.g. a YAML with project metadata or previously drafted plans) so GPT can reference the current project’s specifics.

### Instruction Tuning (Language and Tone)

Instructions should emphasize formal, objective government language and the gating mindset (go/no-go, risk, alignment with priorities). We should include style examples. For instance, tell GPT:

- “Use third-person passive tone and avoid first-person.”
- “Each decision question should be framed as an evaluative bullet (‘Has the long list of options been reduced to a shortlist?’ for Gate 1).”

Including sample paragraphs in the prompt (few-shot) can teach the model to mimic the bureaucratic prose seen in official documents. Also, instruct it to generate structured output (Headings, numbered lists, bullet points) consistent with official docs. For example:

- “Use Markdown headings and lists for clarity, as shown in sample gate plan.”

### Memory/State Strategy

Custom GPTs currently do not have persistent memory across sessions. Therefore, we must manage “state” (project ID, user info, previous sections) externally. One approach is to include key project variables in each prompt or knowledge context. For instance, each session can begin by re-stating the project ID, current gate, stakeholders, etc. These can be inserted into the system or user message from a saved context.

Alternatively, the commit tool can return metadata summaries (e.g. last section title committed) which the frontend includes in the chat. Although the GPT builder doesn’t provide memory, we can simulate it: store important variables (project name, decision, gate number) in our backend or as a small “project info” knowledge file that we update. The GPT can then retrieve them by semantic search.

---

## OpenAPI Tooling Schema

We will define custom ChatGPT Actions (tools) using OpenAPI paths. At minimum, we need a commit action to save content to Google Drive. We propose two endpoints:

### POST /commitSection (append a section)

**Parameters:**

- `projectId` (string): Unique project identifier.
- `gateStage` (string): e.g. “Gate 1”, “Gate 2”, etc.
- `sectionTitle` (string): The section or heading name (e.g. “Scope”, “Risk Analysis”).
- `contentMarkdown` (string): The section content in Markdown.
- `userId` (string): Who is committing (for audit).
- `timestamp` (string, ISO8601): When the content was generated.
- `append` (boolean, optional): If true, append to existing section; if false, replace.
- `versionLabel` (string, optional): e.g. “Draft 1” or “Revision 3”.

**Behavior:** Creates or updates the specified section in the project document. Ensures sections are stored in sequence (see FastAPI design).

**Response:** Confirmation with current document URL or ID and version number.

### POST /commitDocument (full document)

**Parameters:** Same metadata plus a single large `contentMarkdown` for the whole document.

**Behavior:** Saves the entire content as one document (useful for final commits or small docs).

**Response:** File identifier and status.

In OpenAPI YAML, these would be defined with appropriate schema objects. For example (excerpt):

```yaml
paths:
  /commitSection:
    post:
      operationId: commitSection
      summary: "Commit a section of a gate document"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                projectId:   { type: string }
                gateStage:   { type: string }
                sectionTitle:{ type: string }
                contentMarkdown: { type: string }
                userId:      { type: string }
                timestamp:   { type: string, format: date-time }
                append:      { type: boolean }
                versionLabel:{ type: string }
              required: [projectId, gateStage, sectionTitle, contentMarkdown]
```
### API Design for Commit and Fetch Actions

We will similarly define `/commitDocument`. These schemas allow ChatGPT to call, for example:

```json
commitSection(
    projectId="123",
    gateStage="Gate 1",
    sectionTitle="Scope",
    contentMarkdown="...",
    userId="userA",
    append=true
)
```

when ready to save content. The GPT should refer to the actions by name exactly (e.g., `commitSection`) as per OpenAI’s advice ([OpenAI Help Center](https://help.openai.com)). We will include example calls in the system instructions so the model uses them correctly (few-shot examples of JSON API calls).

For versioning, the `append` flag or a separate `appendMode` parameter can control whether to add to an existing file or create a new one. If `append=false`, the backend might overwrite or start a new file. We should also support an optional `draftVersion` string so users can label drafts. These fields let us handle both incremental commits (section by section) and final full-document commits.

Optionally, to support external edits, we could define a `GET /fetchDocument` action that returns the latest content for a project/gate. The GPT could call this to ingest user-updated content. For example:

```json
fetchDocument(
    projectId="123",
    gateStage="Gate 1"
)
```

might return all sections. This action is similar to commit but in reverse (read-only).

In summary, the main commit tools include all document content, section metadata, project ID, gate, user, timestamp, and versioning flags. We will ensure the schema is clear so GPT includes all required parameters.

---

## FastAPI Backend Design

### Route Handling and Chunking

Our FastAPI backend will implement the above routes. When `/commitSection` is called, we will chunk or buffer sections appropriately. One approach is: maintain an in-memory or database record for each project’s document-in-progress, keyed by `(projectId, gateStage)`. Each call to `commitSection` will append that section to the record (or reorder based on `sectionTitle`). Internally, we can store each section as a separate entry (with an index), then join them in order when needed. Alternatively, we can open a Google Drive file in append mode each time (using Drive’s append or update API). For reliability, we might write locally first (Markdown files per section) and then push to Drive when all sections are committed. Sections should be stored in order. We might include an implicit section index (order of calls), or use the title to sort (if numbered). 

The backend must guard against concurrency issues: if two sections come in simultaneously, ensure one doesn’t overwrite the other. We could use optimistic locking or simply queue commits per project.

### Secure Storage in Google Drive

For the POC, we will use Google Drive via its API. The FastAPI server should use OAuth 2.0 (service account or user credentials) to authenticate to Drive. All API calls must use HTTPS and proper auth tokens. To secure documents, we should create (or specify) a Drive folder for each project. Only authorized accounts (the service account and project stakeholders) should have access. File sharing settings should be locked down. We will handle tokens securely (not hard-coding them; possibly using Google’s recommended libraries or an OAuth flow).

### Document Lifecycle

We anticipate a lifecycle: **Draft → Commit → Versioning → Finalize**. Initially, content is in-draft within GPT chat. Each `commitSection` moves content to a draft document in Drive or staging storage. We should mark drafts distinctly (e.g. file name `Project123_Gate1_Draft1`). On each commit we may increment a draft version. Using Drive’s revision feature, we can keep a full history: 

> “Drive API provides the revisions resource so that you can download and publish file revisions” ([Google Drive API Documentation](https://developers.google.com/drive/api/guides/manage-revisions)).

We can call the Drive Revisions API to list previous versions or to lock them. When the user signals finalization, we can mark the draft as final (e.g. remove “Draft” from the name or set a metadata flag). We could then use Drive to publish the final version or export it. Once finalized, further commits should either be prevented or go into a new version. 

We should design the FastAPI to handle a flag like `finalize=true` on the last commit, which triggers conversion/export and prevents further editing.

### File Conversion

If a PDF/Word output is needed, FastAPI can convert. Options include using a library like Pandoc to convert Markdown to PDF or DOCX, or using Google Drive itself: if we save content as a Google Doc, we can use Drive’s `files.export` to get a PDF/Word file. For example, after finalizing, the API can call `files.export(fileId, mimeType='application/pdf')` to generate a PDF. 

We should include an endpoint (or a parameter on finalize) for these conversions. This allows a command like `finalize=true, exportFormats=["pdf","docx"]` in our schema. Conversion should happen asynchronously, with logging of progress or errors.

### Logging and Error Handling

Given large documents, the backend needs robust logging. All tool calls (incoming commit requests) should be logged with timestamps. If an error occurs (e.g. Drive quota exceeded, content too large), the API should catch it and return an error message to ChatGPT. For example, if Google API returns `413` (too large), the backend can respond with a clear error that GPT can relay. 

We should break uploads into chunks if needed (Drive chunked upload) to avoid failures. Each step (append section, finalize, export) should log successes and failures. Failures should be communicated so that the GPT can ask the user to try again or break into smaller parts.

---

### Document Management Integration

#### Google Drive Structure and Metadata

We will organize Drive with a clear folder and metadata scheme. For example, create a folder for each project (named by Project ID or name). Within it, we can have subfolders or files for each gate stage (e.g. “Gate 1 Document”, “Gate 2 Document”). The `projectId` and `gateStage` from the tool calls map directly to folder names. We will store the document as a Google Doc (or Markdown file) with meaningful names like `Proj123_Gate1_Document`.

To sync metadata, we will use Google Drive’s custom file properties. Drive allows setting `appProperties` (key-value metadata) on files ([Google Drive API Documentation](https://developers.google.com/drive/api/guides/properties)). We will tag each file with keys like:

- `projectId: "Proj123"`
- `gateStage: "Gate1"`
- `version: "1"`

This ensures we can query or search files by these properties. For instance, on commit the API will call:

```json
files.update(..., appProperties={"projectId":..., "gateStage":..., "version":...})
```

This metadata will mirror our project tracking. The user’s identity (from our system) can also be stored as a property if needed. Using properties, the GPT or user can later fetch this metadata to know the document’s context (e.g. “File current version is Draft2 for Gate 1”).

#### Round-Trip Architecture (Canvas ↔ Drive)

In Canvas mode, the user interacts in ChatGPT, and content flows one-way from GPT to Drive via commits. In external mode, the user might open the Drive document, edit it (perhaps collaboratively), then want ChatGPT to re-incorporate those changes. To support this, we can implement a `fetchDocument` action (or instruct the user to copy the updated content into the chat). For example, the user could prompt:

> “GPT, I’ve updated the Scope section in Google Docs. Can you incorporate the changes?”

The model can then either request the updated content via the `fetchDocument` tool (if implemented) or ask the user to paste the new text. Once the content is back in GPT, the model can summarize differences or merge into the final draft and then call `commitSection` again to update the file.

In practice, we might not automate the fetch (for POC it may suffice to have the user paste). But the schema can include a `fetchDocument(projectId, gateStage)` so that ChatGPT can pull the latest from Drive when needed.

#### Synchronization and UX Flow

The user experience should clearly support both modes. In Canvas mode, the user simply asks GPT to write sections and commit. In external mode, GPT can prompt:

> “It looks like you edited the document outside. Should I pull the latest content? If so, please provide the updated text or call fetchDocument.”

After pulling, GPT can say:

> “I have the updated content for Section X. Do you want a summary of changes or a revised section draft?”

This guidance can be built into the prompt templates.

For metadata and gating info, each Drive folder/file can include tags or text in the document body (e.g. a header “Gate 1 – Draft”). The GPT should always know (from its prompt/context) which gate it’s working on, and ensure the Drive metadata matches. For example, when committing Gate 2 content, the API sets:

```json
appProperties: {gateStage: "Gate2"}
```

We can also organize files by folder hierarchy: one folder per project, subfolders “Gate1”, “Gate2”, etc. The API can create these folders on demand. By combining structured file naming, Drive properties, and internal records, the system will keep the document metadata synchronized with project state. For instance, after finalizing Gate 1, we might set:

```json
appProperties: {status: "Final"}
```

and move the file to a “Closed Gates” folder.

---

### UX Support for Hybrid Editing

#### Canvas Mode

In this mode, the user never leaves ChatGPT. They might converse: 

> “Write the Risk Analysis section of the Gate 2 plan.”

PolicyGPT generates it, then the user asks:

> “Commit this to the document.”

PolicyGPT then calls `commitSection`. The response can confirm:

> “Section committed. Document now has X pages.”

The chat can show GPT asking for next steps. This mode is straightforward: each commit is a dialogue step. We must ensure GPT prompts the user at logical points (e.g., “Would you like me to start the next section or make revisions?”).

#### External Edit Mode

Here, after generating a section (or full document), the user might want to refine it in Google Docs. The workflow could be:

1. GPT generates and commits a draft.
2. User opens the file via Drive link and edits offline.
3. In chat, the user says:

    > “I’ve made changes to Section Y.”

PolicyGPT should then either fetch or ask for the updated text, and then incorporate it. For instance, after user input, GPT could say:

> “Understood. Please paste the revised section here for me to integrate.”

Once it has the new content, GPT can either replace the section in-memory and commit again or summarize differences if needed.

#### Prompting for Edits

The GPT’s instructions should include checks for this scenario. It could say:

> “After completing each section, ask the user: ‘Would you like to review or edit this section externally?’ If yes, instruct them on how to provide edits.”

Also, we can teach the GPT to use a summarization prompt:

> “Use `summarizeDocument(content=…)` to condense long sections or highlight changes.”

(If we implement such a tool, GPT would call it with the full updated text to get a summary.) The user can then accept or refine the summary.

#### Round-Trip Architecture

Technically, when GPT calls `commitSection`, the FastAPI takes the content and updates Drive. When the user edits in Drive, the file ID remains the same, so a subsequent `fetchDocument` can retrieve it. Thus the cycle is:

1. GPT → Drive (commit) → 
2. User edits → 
3. GPT (fetch/summarize) → 
4. Drive (re-commit).

We should ensure the API returns the Drive file ID or URL on commit so the user can easily open it. Possibly the commit response can include a hyperlink (Drive URL) to the file.

#### Error Scenarios

If the user edits externally while GPT was generating other sections, there may be version conflicts. We should design the API to check if a file has changed since the last commit (using Drive revisions or timestamps). If GPT tries to commit an outdated version, the API can warn:

> “A newer draft exists on Drive. Do you want to overwrite or merge?”

The GPT can then ask the user.

#### Metadata Synchronization

As content moves back and forth, ensure the project and gate metadata remain aligned. The GPT should not change the project ID or gate stage mid-stream; these are fixed once set in the conversation. Every commit or fetch should include these fields. The Drive files can have a custom field (`appProperty`) like `lastEditor=GPT` or `lastEditedBy=UserX` if needed for auditing, but at minimum, we track version.

---

In summary, UX considerations include clear prompts at each step (e.g., after each commit ask “Next section?”), guidance when leaving Canvas (“You can open the document here...”), and support for the user returning content to GPT for review. The architecture ensures any content in ChatGPT can be pushed to Drive and vice versa, with metadata kept in sync via file properties.


---

## References

- [Guide to Project Gating - Canada.ca](https://www.canada.ca/en/treasury-board-secretariat/services/information-technology-project-management/project-management/guide-project-gating.html)
- [Knowledge in GPTs | OpenAI Help Center](https://help.openai.com/en/articles/8843948-knowledge-in-gpts)
- [Key Guidelines for Writing Instructions for Custom GPTs | OpenAI Help Center](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts)
- [Manage file revisions | Google Drive | Google for Developers](https://developers.google.com/drive/api/guides/manage-revisions)
- [Add custom file properties | Google Drive | Google for Developers](https://developers.google.com/drive/api/guides/properties)
