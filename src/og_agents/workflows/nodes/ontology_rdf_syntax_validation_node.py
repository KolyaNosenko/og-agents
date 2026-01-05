from langgraph.runtime import Runtime

from src.og_agents.prompts import OntologyRDFSyntaxValidationResultPrompt
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState
from src.og_agents.ontology.validators import OntologyRDFSyntaxValidator

NODE_NAME = 'ontology_rdf_syntax_validation'

class OntologyRDFSyntaxValidationNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState | None:
        language_model = runtime.context.language_model
        validator = OntologyRDFSyntaxValidator()
        ontology_ttl = state.get('ontology_ttl')

        result = validator.validate_ttl(ontology_ttl)

        if result.is_valid():
            print('Ontology RDF syntax valid!!')
            return

        prompt = OntologyRDFSyntaxValidationResultPrompt().format(
            ontology_ttl=ontology_ttl,
            validation_result=result
        )

        print("Start fixing RDF syntax:")
        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        print("Ontology fixed:", ontology_ttl)

        return {
            'ontology_ttl': ontology_ttl
        }

