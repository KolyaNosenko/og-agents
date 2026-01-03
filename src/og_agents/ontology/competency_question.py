from pydantic import BaseModel, Field

class CompetencyQuestion(BaseModel):
    """Питання компетентності до онтології"""
    text: str = Field(description="Текст питання компетентності")
