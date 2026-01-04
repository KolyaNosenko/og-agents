from langgraph.runtime import Runtime

from src.og_agents.prompts import OntologyConsistencyValidationResultPrompt
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState
from src.og_agents.ontology.validators import OOPSOntologyValidator, OntologyConsistencyValidator

NODE_NAME = 'ontology_consistency_validation'

class OntologyConsistencyValidationNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState | None:
        language_model = runtime.context.language_model
        validator = OntologyConsistencyValidator()
        ontology_ttl = state.get('ontology_ttl')

        result = validator.validate_ttl(ontology_ttl)

        print('Ontology consistency validation started')

        if result.is_valid():
            print('Ontology consistent!!')
            return

        prompt = OntologyConsistencyValidationResultPrompt().format(
            ontology_ttl=ontology_ttl,
            validation_result=result
        )

        print('Ontology consistency fixing prompt!!!', prompt)

        print("Start fixing ontology:")
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology fixed:", ontology_ttl)

        return {
            'ontology_ttl': ontology_ttl
        }

