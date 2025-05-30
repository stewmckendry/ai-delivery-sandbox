import yaml
import shutil

# List of tool keys to keep
tools_to_keep = [
    "uploadTextInput",
    "uploadFileInput",
    "uploadLinkInput",
    "loadCorpus",
    "queryCorpus",
    "inputPromptGenerator",
    "ingestInput",
    "generateSectionChain",
    "webSearch",
    "goc_alignment_search",
    "assembleArtifactChain",
    "revise_section_chain",
    "generate_artifact_chain",
    "generate_global_context_chain",
    "fetch_artifact_chunk",
    "save_artifact_chunks",
    "section_review_fetcher",
    "record_research"
]

src = "project/reference/tool_catalog.yaml"
dst = "project/reference/tool_catalog_gpt.yaml"

# Step 1: Copy the original file
shutil.copyfile(src, dst)

# Step 2: Filter tools
with open(dst, "r") as f:
    data = yaml.safe_load(f)

filtered_tools = {k: v for k, v in data["tools"].items() if k in tools_to_keep}
data["tools"] = filtered_tools

with open(dst, "w") as f:
    yaml.dump(data, f, sort_keys=False)