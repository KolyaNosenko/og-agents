from pydantic import BaseModel, Field
from og_agents.ontology.competency_question import CompetencyQuestion

class CompetencyQuestions(BaseModel):
    """Список питань компетентності до онтології"""
    questions: list[CompetencyQuestion] = Field(description="Список питань компетентності")

