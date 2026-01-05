from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer

from og_agents.prompts import OntologyRDFSyntaxValidationResultPrompt
from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState
from og_agents.ontology.validators import OntologyRDFSyntaxValidator

ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME = 'ПЕРЕВІРКА_RDF_СИНТАКСИСУ'

class OntologyRDFSyntaxValidationNode(BaseNode):
    def __init__(self):
        super().__init__(ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState | None:
        language_model = runtime.context.language_model
        validator = OntologyRDFSyntaxValidator()
        stream_writer = get_stream_writer()

        print('Ontology RDF syntax validation started')
        stream_writer({
            "current_step": ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
            'message': 'Початок перевірки синтаксису RDF...'
        })

        ontology_ttl = state.get('ontology_ttl')
        result = validator.validate_ttl(ontology_ttl)

        if result.is_valid():
            print('Ontology RDF syntax valid!!')
            stream_writer({
                "current_step": ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
                'message': 'Синтаксис RDF валідний.'
            })
            return

        prompt = OntologyRDFSyntaxValidationResultPrompt().format(
            ontology_ttl=ontology_ttl,
            validation_result=result
        )

        stream_writer({
            "current_step": ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
            'message': 'Синтаксис RDF невалідний.',
            'error': result.error_message
        })

        print("Start fixing RDF syntax:")
        stream_writer({
            "current_step": ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
            'message': 'Початок виправлення синтаксису...',
        })
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology fixed:", ontology_ttl)
        stream_writer({
            "current_step": ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
            'message': 'Онтологію виправлено.',
            'ontology_ttl': ontology_ttl,
        })

        return {
            'ontology_ttl': ontology_ttl
        }

