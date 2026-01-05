from langgraph.runtime import Runtime
from langgraph.config import get_stream_writer

from og_agents.prompts import GenerateCompetencyQuestionsPrompt
from og_agents.workflows.workflow_context import WorkflowContext
from og_agents.workflows.nodes.base_node import BaseNode
from og_agents.state import GenerationState

GENERATE_COMPETENCY_QUESTIONS_NODE_NAME = 'ГЕНЕРАЦІЯ_ПИТАНЬ_КОМПЕТЕНТНОСТІ'

class GenerateCompetencyQuestionsNode(BaseNode):
    def __init__(self):
        super().__init__(GENERATE_COMPETENCY_QUESTIONS_NODE_NAME)

    def __call__(self, state: GenerationState, runtime: Runtime[WorkflowContext]) -> GenerationState:
        language_model = runtime.context.language_model
        documents = state.get('documents')
        prompt = GenerateCompetencyQuestionsPrompt().format(documents)
        stream_writer = get_stream_writer()

        stream_writer({
            "current_step": GENERATE_COMPETENCY_QUESTIONS_NODE_NAME,
            'message': 'Початок генерації питань компетентності...'
        })
        print("Start generating competency questions!")

        response = language_model.invoke(prompt)
        competency_questions = response.content

        stream_writer({
            "current_step": GENERATE_COMPETENCY_QUESTIONS_NODE_NAME,
            'message': 'Питання компетентності згенеровано.',
            'competency_questions': competency_questions,
        })
        print('competency questions:', competency_questions)

        return {
            'competency_questions': competency_questions
        }
