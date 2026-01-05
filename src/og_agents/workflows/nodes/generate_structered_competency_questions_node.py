from langgraph.runtime import Runtime

from og_agents.prompts import GenerateCompetencyQuestionsPrompt
from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState
from og_agents.ontology import CompetencyQuestions

NODE_NAME = 'generate_competency_questions'

class GenerateCompetencyQuestionsNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        language_model = runtime.context.language_model
        documents = state.get('documents')
        prompt = GenerateCompetencyQuestionsPrompt().format(documents)

        language_model_with_structured = language_model.with_structured_output(CompetencyQuestions)
        response = language_model_with_structured.invoke(prompt)

        return {
            'competency_questions': response.questions
        }
