from langgraph.runtime import Runtime

from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState

NODE_NAME = 'ontology_reasoner_node'

class OntologyReasonerNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        print('Ontology reasoner node')
        return
