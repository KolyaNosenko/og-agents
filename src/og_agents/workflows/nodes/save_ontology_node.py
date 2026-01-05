from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer

from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState

SAVE_ONTOLOGY_NODE_NAME = 'ЗБЕРЕЖЕННЯ_ОНТОЛОГІЇ'

class SaveOntologyNode(BaseNode):
    def __init__(self):
        super().__init__(SAVE_ONTOLOGY_NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> None:
        ontology_storage = runtime.context.ontology_storage
        stream_writer = get_stream_writer()

        ontology_ttl = state.get('ontology_ttl')

        stream_writer({
            "current_step": SAVE_ONTOLOGY_NODE_NAME,
            'message': 'Збереження онтології...'
        })
        print('Saving ontology:', ontology_ttl)

        ontology_storage.create_from_ttl(ontology_ttl)
        stream_writer({
            "current_step": SAVE_ONTOLOGY_NODE_NAME,
            'message': 'Онтологію збережено!'
        })

