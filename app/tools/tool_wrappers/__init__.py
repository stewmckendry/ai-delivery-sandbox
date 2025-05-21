# Tool wrappers are dynamically loaded by tool_registry.py
# Each should define a class Tool with a method run_tool(input_dict)

# Standard wrapper pattern:
# class Tool:
#     def run_tool(self, input_dict):
#         self.validate(input_dict)
#         ...