📁 **Repository**: `ai-delivery-sandbox`
🌿 **Branch**: `sandbox-curious-falcon`
🎯 **Objective**: Reverse-engineer this legacy-style repo to extract software artifacts that can support migration, reimplementation, or documentation of the current system.

⚠️ **Important Context**:
- The repo includes both current and outdated code.
- Files and folders may be inconsistently organized or labeled.
- There may be dead code or placeholders.

Please assume the goal is to preserve or replicate current behaviour in a future implementation.

📌 **Strategy**:
1. **Scan** the repo structure to identify the main entry points and active logic.
2. **Focus** only on complete or recently modified components.
3. **Ignore** obviously outdated, empty, or placeholder files.

🧠 **Analyze and Generate the Following Outputs**:

### 1. 🧾 User Stories @ Definition of Ready
For all key capabilities inferred from the codebase:
- Format: *As a [user], I want [function] so that [benefit]*
- Include Acceptance Criteria (bullet or Gherkin-style)
- Note assumptions or gaps where the code is unclear
- Call out any dependencies (data, APIs, interfaces)

### 2. 🛠️ Design Decomposition
Split design insight into 3 distinct categories:
- **Technical Design:** Modules, services, scripts, external libraries
- **Interface Design:** UI routes, endpoints, CLI commands, internal/external APIs
- **Data Design:**
  - *Flows:* how and where data moves through the system
  - *Schema:* inferred structure or objects used across components

### 3. ✅ Test Suite Outline
Provide a test strategy including:
- High-level scenarios (system-level black box)
- Component-level test ideas
- Data integrity/validation checks

### 4. 🧭 Modernization Opportunities
Optional: Suggest opportunities for improvement or refactoring based on observed design/code patterns.  
(Note: no new system/modules exist yet — this is purely for future planning.)

📝 **Output Format**:
Return a clear, structured markdown summary of these 4 outputs. Use sections and subheadings to improve readability.