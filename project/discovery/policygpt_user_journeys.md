# PolicyGPT User Personas and Journey

## User Personas

### 1. Policy Analyst or Project Manager (Gate Artifact Owner)
- **Role**: Responsible for preparing gate artifacts (e.g., investment proposals, business cases).
- **Needs**: Speed up the process of drafting and refining gate documents, ensure compliance with standards, reduce manual formatting and rework.
- **Pain Points**: High cognitive load, inconsistent templates, frequent reviewer feedback cycles, and pressure to meet deadlines.
- **PolicyGPT Support**:
  - Provides authoritative templates and examples.
  - Auto-generates draft sections using uploaded content.
  - Offers structured prompts to guide input collection.
  - Maintains alignment with official gating criteria and language.
  - Prompts user to include evidence-based justifications and references.

### 2. Director or Executive Reviewer (Indirect User)
- **Role**: Reviews and approves draft documents, ensures strategic alignment and risk management.
- **Needs**: Clear, complete, and well-structured submissions that support confident decision-making.
- **Pain Points**: Receiving incomplete or misaligned drafts, difficulty tracking iterations.
- **PolicyGPT Support**:
  - Enables their feedback to be incorporated via uploads.
  - Provides summaries and decision logs to primary users.

### 3. External Partner (Indirect User)
- **Role**: Supports preparation of documentation, may draft or review content externally.
- **Needs**: Access to project context, structured outputs, ability to contribute drafts.
- **Pain Points**: Onboarding time, access to files and guidance.
- **PolicyGPT Support**:
  - Provides structured guidance to primary users.
  - Accepts external edits re-ingested into the workflow.

## User Journeys

### Journey A: Structured Iteration (Primary Path)
1. **User** says they need to prepare artifacts for Gate 0.
2. **PolicyGPT**:
   - Looks up requirements from reference files (artifacts, templates, inputs, criteria).
   - Presents a checklist and links to templates.
   - Asks user for known inputs and suggests where to find the rest.
3. **User** uploads interview transcripts, notes, and existing docs.
4. **PolicyGPT**:
   - Reads files.
   - Synthesizes inputs.
   - Maps to artifact sections.
   - Generates a draft outline, then expands one section at a time.
   - Prompts users again if critical data, rationale, or citations are missing.
   - RACI roles, governance templates, and stakeholder responsibilities are embedded within specific artifact sections.
   - Metadata (section type, gate number, draft status) is attached with each commit using `commitSection` to Google Drive.
   - Maintains coherence across sections using a centralized YAML project profile (goals, scope, risks, stakeholders) that informs all content generation.
5. **User and GPT** iterate section by section using GPT canvas.
6. **User** may export to Docs, edit externally, and return revised content.
7. **GPT** integrates revisions and uses outline continuity (alignment to structure, section order, and transitions) to ensure logical flow when stitching sections into a full document for user review.
8. **User** previews full draft in GPT canvas before finalization.
9. **GPT** commits final document to Google Drive and provides versioned links with reviewer initials and gate status.

### Journey B: "Check-the-Box" Generation (Fast Track)
1. **User** uploads required inputs and says "Generate complete gate document."
2. **PolicyGPT**:
   - Generates outline.
   - Uses the sectioning/chunking method from Journey A to sequentially generate each artifact section.
   - Inserts default risk/privacy templates where required.
   - Applies redaction flags (e.g., sensitive internal content) and version labels.
   - Commits each section or final doc to Google Drive.
3. **User** previews and downloads the document for submission.

### Journey C: Review and Revise
1. **User** uploads feedback from reviewers.
2. **PolicyGPT** reads and synthesizes feedback.
3. **PolicyGPT** updates sections, highlights key changes, and preserves original context.
4. **User** accepts updates or provides additional input.

## Technical and Content Enhancements from Specification
- **Hierarchical Outline**: Ensures structure and completeness.
- **Chunking**: One section at a time to manage token limits.
- **Reference Files**: YAML + docs used in knowledge layer.
- **Prompt Tuning**: Formal tone, bureaucratic prose, labeled sections.
- **Hybrid Edit Support**: Commit content, fetch changes, integrate revisions.
- **Audit and Metadata**: Every commit logs user, time, gate, and version.
- **Commit Links**: Each section and document commit returns Google Drive URL.
- **Approvals History**: Tracks who signed off and when with document status.
- **Bilingual Outputs**: Option for dual-column or translation prompts.
- **Security/Privacy Templates**: Auto-included where mandatory.
- **Evidence-Based Checks**: Prompts for evidence and alignment with strategic goals.
- **Preview Mode**: User sees draft before commit to ensure accuracy.
- **Input Guidance**: Tooltips or prompts guide user on "good" input standards.

## Comparison to Current Process
| Current State | With PolicyGPT |
|---------------|-----------------|
| Ad hoc templates | Standardized artifact templates |
| Manual synthesis | Auto synthesis and formatting |
| Heavy feedback loops | Iterative, versioned collaboration |
| Disconnected tools | Integrated with Git and Drive |
| Unstructured governance capture | Built-in RACI and endorsement scaffolds |
| Minimal audit history | Full audit logs and metadata for each draft |

## Comparison to Using Standalone GPT
| Standalone GPT | PolicyGPT |
|----------------|-------------|
| Generic outputs | Gate-specific formal outputs |
| No memory | Simulated memory with knowledge/context |
| No integrations | Git + Drive integration with commit tools |
| Limited structure | Guided outline + chunked generation |
| No traceability | Versioning, logs, and metadata |
| No security/privacy scaffolds | Built-in risk and privacy sections |

## My Thoughts
- **Value**: High. Reduces manual effort, improves quality and compliance.
- **Feasibility**: Realistic using current OpenAI + Google APIs.
- **Opportunities to Improve**:
  - Add preview mode before commit.
  - Add user guidance on what “good” inputs look like.
  - Consider real-time co-editing with Docs for hybrid collaboration.
  - Enhance routing for interdepartmental review flows.
  - Build redaction tools and status tagging for political sensitivity.

This approach reflects user needs, aligns with the implementation spec, embeds critical process requirements from project goals, and ensures robust, transparent, and auditable artifact creation.
