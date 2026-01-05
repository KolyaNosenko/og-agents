from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel
from src.og_agents.common.http_client import HttpClient
from src.og_agents.config import AppConfig
from src.og_agents.ontology import OntologyStorage


@dataclass
class WorkflowContext:
    config: AppConfig
    http_client: HttpClient
    # TODO add custom type
    language_model: BaseChatModel
    ontology_storage: OntologyStorage
