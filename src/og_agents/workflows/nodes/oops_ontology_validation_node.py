from langgraph.runtime import Runtime

from src.og_agents.prompts import OOPSValidationResultPrompt
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState
from src.og_agents.ontology.validators import OOPSOntologyValidator

NODE_NAME = 'oops_ontology_validation'

class OOPSOntologyValidationNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState | None:
        language_model = runtime.context.language_model
        http_client = runtime.context.http_client
        config = runtime.context.config
        validator = OOPSOntologyValidator(http_client=http_client, config=config)
        ontology_ttl = state.get('ontology_ttl')

        result = validator.validate_ttl(ontology_ttl)

        if result.is_valid():
            return

        prompt = OOPSValidationResultPrompt().format(
            ontology_ttl=ontology_ttl,
            validation_result=result
        )

        print('Ontology OOPS fixing prompt!!!', prompt)

        print("Start fixing ontology:")
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology fixed:", ontology_ttl)

        return {
            'ontology_ttl': ontology_ttl
        }

