from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer

from og_agents.prompts import OOPSValidationResultPrompt
from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState
from og_agents.ontology.validators import OOPSOntologyValidator

OOPS_ONTOLOGY_VALIDATION_NODE_NAME = 'ПЕРЕВІРКА_ІНСТРУМЕНТОМ_OOPS'

class OOPSOntologyValidationNode(BaseNode):
    def __init__(self):
        super().__init__(OOPS_ONTOLOGY_VALIDATION_NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState | None:
        language_model = runtime.context.language_model
        http_client = runtime.context.http_client
        config = runtime.context.config
        validator = OOPSOntologyValidator(http_client=http_client, config=config)
        stream_writer = get_stream_writer()

        stream_writer({
            "current_step": OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
            'message': 'Початок перевірки онтології інструментом OntOlogy Pitfall Scanner...'
        })

        ontology_ttl = state.get('ontology_ttl')
        result = validator.validate_ttl(ontology_ttl)

        if result.is_valid():
            print('Ontology valid!!')
            stream_writer({
                "current_step": OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
                'message': 'Онтологія успішно проходить всі перевірки.'
            })
            return

        prompt = OOPSValidationResultPrompt().format(
            ontology_ttl=ontology_ttl,
            validation_result=result
        )

        stream_writer({
            "current_step": OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
            'message': 'Онтологія містить зауваження',
            'error': result.error_message
        })

        print('Ontology OOPS fixing prompt!!!', prompt)

        print("Start fixing ontology:")
        stream_writer({
            "current_step": OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
            'message': 'Виправлення зауважень...',
        })
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology fixed:", ontology_ttl)
        stream_writer({
            "current_step": OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
            'message': 'Онтологію виправлено.',
            'ontology_ttl': ontology_ttl,
        })

        return {
            'ontology_ttl': ontology_ttl
        }

