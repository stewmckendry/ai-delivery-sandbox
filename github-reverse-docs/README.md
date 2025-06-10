# GitHub Reverse Engineering PoC

## Objective
Explore how GPT connectors can be used to extract software requirements, design components, and test scripts by analyzing codebases in GitHub.

## Target Audience
IT and engineering teams modernizing legacy systems.

## Hypothesis
We can reduce manual effort in documenting monolithic, undocumented systems by reverse-engineering documentation directly from the code.

## Inputs
- GitHub repo with legacy code (can start with a sample repo)

## Flow
1. Connect to GitHub repo
2. Fetch codebase files
3. Analyze using GPT to extract:
   - Business requirements
   - Architectural design
   - Test scripts / scenarios

## Output
Structured markdown or PDF documentation draft.

## Notes
Start small with one file or module, and grow the scope as needed.