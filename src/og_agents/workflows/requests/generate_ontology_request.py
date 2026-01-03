from typing import TypedDict

from src.og_agents.documents import OntologySourceDocument

class GenerateOntologyRequest(TypedDict):
    documents: list[OntologySourceDocument]
