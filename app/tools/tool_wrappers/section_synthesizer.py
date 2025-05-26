class Tool:
    def run_tool(self, inputs: dict) -> str:
        memory = inputs.get("memory", [])

        context_lines = []
        for entry in memory:
            if "input_summary" in entry and "full_input_path" in entry:
                context_lines.append(f"- {entry['input_summary']}: {entry['full_input_path']}")
            elif "title" in entry and "url" in entry:
                context_lines.append(f"- {entry['title']}: {entry['url']}")

        context_str = "\n".join(context_lines)

        return f"## Draft Section\n\nContext:\n{context_str}\n\n(TODO: synthesize content from above)"