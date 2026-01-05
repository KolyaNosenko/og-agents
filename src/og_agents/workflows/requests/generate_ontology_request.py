from typing import TypedDict

from og_agents.documents import OntologySourceDocument

class GenerateOntologyRequest(TypedDict):
    documents: list[OntologySourceDocument]
