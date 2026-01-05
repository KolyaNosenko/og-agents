from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer

from og_agents.prompts import GenerateOntologyPrompt
from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState

GENERATE_ONTOLOGY_NODE_NAME = 'ГЕНЕРАЦІЯ_ОНТОЛОГІЇ'

class GenerateOntologyNode(BaseNode):
    def __init__(self):
        super().__init__(GENERATE_ONTOLOGY_NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        language_model = runtime.context.language_model
        stream_writer = get_stream_writer()

        competency_questions = state.get('competency_questions')
        documents = state.get('documents')
        prompt = GenerateOntologyPrompt().format(competency_questions, documents)

        print("Start ontology generation from competency questions:")
        stream_writer({
            "current_step": GENERATE_ONTOLOGY_NODE_NAME,
            'message': 'Початок генерації онтології з питань компетентності...'
        })
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology generated:", ontology_ttl)
        stream_writer({
            "current_step": GENERATE_ONTOLOGY_NODE_NAME,
            'message': 'Онтологію згенеровано',
            'ontology_ttl': ontology_ttl,
        })

        return {
            'ontology_ttl': ontology_ttl
        }