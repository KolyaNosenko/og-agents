from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel


@dataclass
class WorkflowContext:
    # TODO add custom type
    language_model: BaseChatModel