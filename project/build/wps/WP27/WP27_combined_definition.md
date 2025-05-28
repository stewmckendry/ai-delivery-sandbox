## WP27 – End-to-End Experience Integration + Iterative Enhancement

## 🧠 What is PolicyGPT?

PolicyGPT is an AI-powered assistant designed to support teams in drafting high-quality gating artifacts for technology delivery. It integrates a custom GPT interface with a curated set of backend tools and memory systems that allow users to iteratively generate, revise, and assemble the components of approval-ready documents.

Unlike traditional documentation workflows, PolicyGPT offers a conversational, guided experience that adapts to user input, project context, and policy frameworks. It aims to accelerate artifact creation while maintaining the depth, structure, and traceability required by reviewers and approvers.

### 📘 Status
The core doc generation tools and toolchains are complete and offer a powerful foundation. However, we haven’t yet wired them into the actual GPT interface and tested how realistic and fluid the experience is for a real-world user generating a policy gate artifact.

Tooling is well-designed but scattered across wrappers and chains. The journey a user takes from idea to document is fragmented and lacks holistic validation.

### 🚀 Your Mission
Create a frictionless and realistic user experience for generating policy artifacts using the existing tools and toolchains. Jam on the best UX by iteratively testing and evolving the system with real user flows and GPT integration.

This WP owns:
- Connecting the GPT interface to toolchains + tools
- Executing realistic user journeys end-to-end
- Documenting feedback, friction points, and enhancement needs
- Iterating rapidly to improve experience, accuracy, and modularity

### 🔍 Grounding in the Real User Journey

Before designing an optimized experience with PolicyGPT, it's essential to understand the current reality for a PM responsible for creating gating artifacts—such as an Investment Proposal for Gate Zero.

#### 🧭 The Baseline PM Journey (Without PolicyGPT)

If a PM were tasked with submitting a Gate Zero artifact by Friday to meet a board deadline, the steps might look like this:

1. **Clarify Expectations**:
   - Look up the gate requirements.
   - Identify the required artifact (e.g., Investment Proposal).
   - Review content criteria and guidance.

2. **Build a Personal Workplan**:
   - Develop a plan to deliver by Friday.
   - Break down work into research, drafting, review, and submission.

3. **Conduct Research**:
   - **Internal Policy Corpus**: Locate relevant policies, strategies, guidelines, and mandate letters.
   - **Program Inputs**: Gather notes from meetings, workshop outputs, prior reports, and other source material.
   - **Benchmarking**: Identify “gold star” examples of successful investment proposals.
   - **External Scan**: Research what other jurisdictions or organizations are doing in the space.

4. **Draft the Artifact**:
   - Start with a structured outline.
   - Fill in each section using the curated research.
   - Iterate on the draft through personal edits.

5. **Review and Feedback**:
   - Send draft to key stakeholders via email or shared drive.
   - Collect feedback (often via disjointed email chains).
   - Triaging and synthesizing feedback manually.
   - Iterate and refine the draft accordingly.

6. **Finalize and Submit**:
   - Ensure quality, completeness, and alignment.
   - Submit final draft for board prep.

#### 😣 Pain Points in the Current Journey

- **Fragmented Research**: Slow, manual gathering of diverse, scattered inputs.
- **Manual Drafting**: High cognitive load to synthesize and write from scratch.
- **Disorganized Feedback**: Stakeholder input is decentralized and hard to track.
- **Time Pressure**: PMs often have to compress high-quality work into a short time frame.

This is the **baseline experience** that PolicyGPT aims to improve—and eventually reimagine.

#### ✨ Design Principle: Meet the User Where They Are

In WP27, we’ll start each design/testing iteration by anchoring on this real-world PM journey. For each iteration, we’ll:

- Pick a **natural slice of the user flow** (e.g., uploading research inputs, generating a section, sending for review).
- Choose tools and toolchains from the [tool catalog](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/reference/tool_catalog.yaml) to support that slice.
- Test and refine them through actual end-to-end use.
- Gradually evolve toward a **frictionless, intelligent UX** that handles the hard parts while feeling natural and supportive for the user.

## ⚖️ Design Principle: Balance Between GPT and Backend Tools

One of the core design challenges of PolicyGPT is deciding which capabilities should reside in the custom GPT interface versus which should be handled by backend tools and toolchains.

We aim to leverage the strengths of both:
- **Custom GPT** excels at natural language interaction, flexible reasoning, and context-sensitive guidance.
- **Backend tools** are better suited for structured logic, multi-step workflows, validation, and integration with memory, schemas, and databases.

Our principle is to **deliver the richest, most seamless user experience possible** while ensuring the outputs are high-quality, review-ready artifacts. That means using GPT where it enhances the experience and letting backend tools do the heavy lifting where precision, control, or repeatability is key.


### 🔁 Iterative Approach
Each iteration will:
1. Define a user flow
2. Choose the best toolchains + tools from the [tool_catalog.yaml](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/reference/tool_catalog.yaml)
3. Write a local test script to validate the flow
4. Configure a custom GPT with the OpenAPI schema to support it
5. Test the full user experience
6. Document feedback + enhancement needs
7. Prioritize and implement the fixes for next round

We start with a minimal journey and build outward.

### 📊 Evaluating Outputs in Each Iteration

As we build and test toolchains in WP27, it’s critical that we also evaluate the outputs they generate. This ensures we’re not just building functional pipelines, but ones that produce high-quality, approvable content.

#### 🎯 Evaluation Objective

Ultimately, our bar for success is this: **Could a gate approver read the output and approve it without knowing or caring that it was generated by an AI system?** If the output meets the criteria, is persuasive, and requires minimal rework, we’ve succeeded.

#### 🧪 How We Evaluate

Each iteration should include a simple evaluation process, which may include:

- **Manual Review by Approver (Human Lead)**:
  - Was the content complete and on-topic?
  - Was the tone, structure, and formatting aligned with standards?
  - Would you approve this artifact if it were submitted?

- **AI-Driven Metrics (Where Applicable)**:
  - **BLEU / ROUGE / METEOR**: For comparing generated text against reference examples (if available).
  - **BERTScore**: Measures similarity in meaning using embeddings.
  - **Toxicity / Hallucination Checks**: To detect bias, unsupported claims, or fabrications.

- **Custom PolicyGPT Metrics**:
  - **Approver Confidence Score (0–5)**: A subjective score reflecting reviewer comfort with the output.
  - **Rework Effort Estimate (Low/Medium/High)**: Estimated level of effort to polish the output.
  - **Guideline Coverage**: Did it address all required elements outlined in gate references?

#### 📝 Tips for WP27 Pod

- Keep evaluation light-touch but consistent.
- Log scores + observations in a simple YAML or Markdown file per test.
- Tag outputs with trace IDs so you can link them back to inputs and toolchains.
- Use evaluations to inform which tools/toolchains to enhance or replace in the next iteration.

We’ll evolve our evaluation framework over time, but even simple structured feedback can drive significant improvements and prioritization in early iterations.


### 📦 Deliverables
- Validated, connected toolchains wired into GPT
- Working end-to-end GPT experience for core user scenarios
- Iteration-by-iteration documentation (test plans, configs, feedback)
- Refined toolchains and enhancements based on testing
- Suggested improvements to the tool catalog

## 🚀 Getting Started with WP27

To begin WP27, follow these steps:

1. **Review the Tool Catalog and the Reference Files**  
   Familiarize yourself with the tools and toolchains available in [`tool_catalog.yaml`](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/reference/tool_catalog.yaml). These are your building blocks.

2. **Define a Simple User Flow**  
   Start small. Pick a realistic user flow that someone might follow to begin drafting an artifact.

3. **Select + Enhance Supporting Tools + Toolchains**  
   Based on the flow, choose tools and/or toolchains that support it. If there's gaps, then enhance them to support the flow.

4. **Write a Test Script**  
   Create a local test script that automates the user journey end-to-end using the selected tools.

5. **Set Up Custom GPT**  
   Ensure the GPT is wired with the proper OpenAPI schema to call the tools.

6. **Run End-to-End Tests**  
   Try the flow using GPT, note any friction, bugs, or enhancement ideas.

7. **Evaluate the Outputs**  
   Use a mix of manual review and AI-driven or custom metrics to assess the quality of the outputs. Capture metrics like Approver Confidence, Rework Estimate, and Guideline Coverage to guide enhancements.

8. **Document Learnings + Plan Iteration 2**  
   Capture feedback in the WP27 folder and plan what to build or improve next.

9. **Repeat**  
   Continue to refine flows, enhance tools, and build out the full user journey.

Documentation, test cases, and insights should be saved to the `project/build/wps/WP27` folder.


### 🧪 Local Testing Approach

For effective local testing of PolicyGPT toolchains and individual tools, we recommend using **Python scripts executed via the CLI terminal within VS Code**. This approach provides full control, easy visibility into outputs at each step, and facilitates rapid iteration. Here's how to structure your testing:

1. **Write Standalone CLI Scripts**:
   - Create scripts that sequentially call each tool in a toolchain with sample inputs.
   - Print key outputs and intermediary values after each tool call for transparency.
   - Use `argparse` to parameterize inputs for flexibility.

2. **Use Logging and Console Prints**:
   - Ensure each tool emits structured logs using `logger.debug/info/warn`.
   - Supplement with `print()` statements in early testing for quick feedback.
   - Standardize log formats and use log levels (`info`, `debug`, `error`) to make outputs easier to scan.

3. **Notebook for Visualization (Optional)**:
   - If you need to visualize outputs or explore step-by-step results, use a Jupyter Notebook.
   - Good for detailed debugging and interactive exploration, especially for complex outputs.

4. **Set Up Reusable Test Data**:
   - Create a `test_data/` folder with representative JSON, YAML, and text inputs.
   - Validate tool behavior against this fixed corpus to avoid regressions.

5. **Include Test Metadata in Script Headers**:
   - Clearly document what each test covers, expected outputs, and known caveats.
   - This makes it easier for future pods to reuse or extend your tests.

6. **Example CLI Test Command**:
   ```bash
   python test_generate_section_chain.py --input test_data/sample_project_profile.yaml


### 📂 Reference Files
- Toolchains:
  - `app/engines/toolchains/generate_section_chain.py`
  - `app/engines/toolchains/revise_section_chain.py`
  - `app/engines/toolchains/assemble_artifact_chain.py`
  - `app/engines/toolchains/generate_full_artifact_chain.py`
  - `app/engines/toolchains/IngestInputChain.py`
- Individual Tools:
  - `app/tools/tool_wrappers/inputChecker.py`
  - `app/tools/tool_wrappers/feedback_mapper.py`
  - `app/tools/tool_wrappers/section_synthesizer.py`
  - `app/tools/tool_wrappers/loadCorpus.py`
  - `app/tools/tool_wrappers/section_refiner.py`
  - `app/tools/tool_wrappers/query_prompt_generator.py`
  - `app/tools/tool_wrappers/structured_input_ingestor.py`
  - `app/tools/tool_wrappers/manualEditSync.py`
  - `app/tools/tool_wrappers/mergeSections.py`
  - `app/tools/tool_wrappers/revision_checker.py`
  - `app/tools/tool_wrappers/formatSection.py`
  - `app/tools/tool_wrappers/confirmProjectProfile.py`
  - `app/tools/tool_wrappers/fetchFromDrive.py`
  - `app/tools/tool_wrappers/text_extractor.py`
  - `app/tools/tool_wrappers/feedback_preprocessor.py`
  - `app/tools/tool_wrappers/section_rewriter.py`
  - `app/tools/tool_wrappers/finalizeDocument.py`
  - `app/tools/tool_wrappers/retry_ingestion.py`
  - `app/tools/tool_wrappers/storeToDrive.py`
  - `app/tools/tool_wrappers/refine_document_chain.py`
  - `app/tools/tool_wrappers/memory_retrieve.py`
  - `app/tools/tool_wrappers/commitArtifact.py`
  - `app/tools/tool_wrappers/uploadLinkInput.py`
  - `app/tools/tool_wrappers/loadSectionMetadata.py`
  - `app/tools/tool_wrappers/uploadTextInput.py`
  - `app/tools/tool_wrappers/uploadFileInput.py`
  - `app/tools/tool_wrappers/web_search.py`
  - `app/tools/tool_wrappers/createSessionSnapshot.py`
  - `app/tools/tool_wrappers/inputPromptGenerator.py`
  - `app/tools/tool_wrappers/goc_alignment_search.py`
  - `app/tools/tool_wrappers/queryCorpus.py`
- Tool Registry + Orchestrator:
  - `app/engines/planner_orchestrator.py`
  - `app/engines/api_router.py`
  - `app/tools/tool_registry.py`
- Catalog:
  - `project/reference/tool_catalog.yaml`
- Gate schema:
  - `project/reference/gate_reference_v2.yaml`
- Project Context:
  - `project/discovery/project_goals.md`

### 📍 Location
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Folder:** `project/build/wps/WP27/`
- **Task ID:** `2.2_build_and_patch`

Let’s build something users actually want to use.