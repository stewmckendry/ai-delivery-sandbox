from app.tools.tool_registry import register_toolchain
from app.tools.tool_wrappers.memory_retrieve import memory_retrieve
from app.tools.tool_wrappers.section_synthesizer import section_synthesizer
from app.tools.tool_wrappers.section_refiner import section_refiner

@register_toolchain("compose_and_cite")
def compose_and_cite_toolchain(context):
    memory = memory_retrieve(context)
    draft = section_synthesizer({"memory": memory})
    refined = section_refiner({"draft": draft})
    return refined