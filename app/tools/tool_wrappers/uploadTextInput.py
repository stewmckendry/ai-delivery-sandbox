from app.utils.input_structuring import structure_input
from app.db.models.ArtifactSection import ArtifactSection

class Tool:
    def run_tool(self, input_dict, log_usage=True, save_profile=True):
        text = input_dict["text"]
        metadata = input_dict.get("metadata") or {}

        if save_profile:
            from app.engines.project_profile_engine import ProjectProfileEngine
            try:
                existing = ProjectProfileEngine().load_profile(metadata["project_id"])
            except:
                existing = {}
            profile = ProjectProfileEngine().generate_profile_from_text(text, metadata, existing)
            ProjectProfileEngine().save_profile(profile)

        entry = structure_input(text, source="direct_input", tool_name="uploadTextInput", metadata=metadata)
        return {"status": "success", "entry": entry}