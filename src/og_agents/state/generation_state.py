from typing import TypedDict, Annotated

from og_agents.documents import OntologySourceDocument
from og_agents.state.reducers import update_documents

class GenerationState(TypedDict):
    documents: Annotated[list[OntologySourceDocument], update_documents]
    # TODO add proper types
    competency_questions: str | None
    ontology_ttl: str | None
