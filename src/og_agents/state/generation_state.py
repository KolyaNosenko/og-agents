from typing import TypedDict, Annotated

from src.og_agents.documents import OntologySourceDocument
from src.og_agents.state.reducers import update_documents

class GenerationState(TypedDict):
    documents: Annotated[list[OntologySourceDocument], update_documents]
    # TODO add proper types
    competency_questions: str | None
    ontology_ttl: str | None
