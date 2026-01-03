from abc import ABC, abstractmethod

from langgraph.runtime import Runtime

from src.og_agents.workflows.workflow_context import WorkflowContext


class BaseNode(ABC):
    _name: str

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def __call__(self, state: dict, runtime: Runtime[WorkflowContext]):
        pass
