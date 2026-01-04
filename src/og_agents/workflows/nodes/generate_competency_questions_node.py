from langgraph.runtime import Runtime

from src.og_agents.prompts import GenerateCompetencyQuestionsPrompt
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes.base_node import BaseNode
from src.og_agents.state import GenerationState

NODE_NAME = 'generate_competency_questions'

class GenerateCompetencyQuestionsNode(BaseNode):
    def __init__(self):
        super().__init__(NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        language_model = runtime.context.language_model
        documents = state.get('documents')
        prompt = GenerateCompetencyQuestionsPrompt().format(documents)

        response = language_model.invoke(prompt)
        competency_questions = response.content

        print('competency questions:', competency_questions)

        return {
            'competency_questions': competency_questions
        }
