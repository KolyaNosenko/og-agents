from langgraph.runtime import Runtime
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState

NODE_NAME = 'save_ontology'

class SaveOntologyNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> None:
        ontology_storage = runtime.context.ontology_storage

        ontology_ttl = state.get('ontology_ttl')

        ontology_storage.create_from_ttl(ontology_ttl)
