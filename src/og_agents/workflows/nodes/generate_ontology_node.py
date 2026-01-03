from langgraph.runtime import Runtime

from src.og_agents.prompts import GenerateOntologyPrompt
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState

NODE_NAME = 'generate_ontology'

class GenerateOntologyNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        language_model = runtime.context.language_model
        competency_questions = state.get('competency_questions')
        documents = state.get('documents')
        prompt = GenerateOntologyPrompt().format(competency_questions, documents)

        result = language_model.invoke(prompt)
        ontology_ttl = result.content

        return {
            'ontology_ttl': ontology_ttl
        }