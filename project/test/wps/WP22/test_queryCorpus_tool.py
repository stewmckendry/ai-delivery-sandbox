import pprint
from app.tools.tool_wrappers.queryCorpus import Tool

# Setup test cases
tests = [
    {
        "name": "T1 - Open government policy objectives",
        "input": {"query": "open government policy objectives"},
    },
    {
        "name": "T2 - Digital services and transparency",
        "input": {"query": "digital services and transparency"},
    },
    {
        "name": "T3 - Canada's open data strategy",
        "input": {"query": "Canada's open data strategy"},
    },
]

# Instantiate the tool
tool = Tool()

# Run tests
for test in tests:
    print(f"\n🔹 Running: {test['name']}")
    try:
        result = tool.run_tool(test["input"])
        pprint.pprint(result)
    except Exception as e:
        print(f"❌ Error in {test['name']}: {e}")