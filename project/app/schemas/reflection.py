from pydantic import BaseModel, Field, validator

class ReflectionInput(BaseModel):
    session_id: str = Field(..., description="Unique ID for the user session")
    career_id: str = Field(..., description="Career being reflected on")
    prompt_id: str = Field(..., description="Prompt that triggered the reflection")
    text: str = Field(..., description="The user’s reflection text")

    @validator("text")
    def check_min_length(cls, value):
        if len(value.strip()) < 10:
            raise ValueError("Reflection must be at least 10 characters long.")
        return value