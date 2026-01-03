from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.og_agents.config import AppConfig
from src.og_agents.state import GenerationState
from src.og_agents.workflows.workflow_context import WorkflowContext
from src.og_agents.workflows.nodes import (
    GenerateCompetencyQuestionsNode,
    GenerateOntologyNode,
    SaveOntologyNode
)
from src.og_agents.workflows.requests import GenerateOntologyRequest


class OntologyGenerationWorkflowBuilder:
    _config: AppConfig
    _state_graph: StateGraph

    def __init__(self, config: AppConfig):
        self._config = config

    @staticmethod
    def create(config: AppConfig) -> 'OntologyGenerationWorkflowBuilder':
        workflow = OntologyGenerationWorkflowBuilder(config)
        workflow._create()

        return workflow

    def build(self) -> CompiledStateGraph[GenerationState, WorkflowContext, GenerateOntologyRequest]:
        if self._state_graph is None:
            # TODO add custom error
            raise Exception('Workflow not initialized')

        return self._state_graph.compile()

    def _create(self):
        self._state_graph = StateGraph(GenerationState)
        generate_cq_node = GenerateCompetencyQuestionsNode()
        generate_og_node = GenerateOntologyNode()
        save_og_node = SaveOntologyNode()

        self._state_graph.add_node(generate_cq_node.name, generate_cq_node)
        self._state_graph.add_node(generate_og_node.name, generate_og_node)
        self._state_graph.add_node(save_og_node.name, save_og_node)

        self._state_graph.add_edge(START, generate_cq_node.name)

        self._state_graph.add_edge(generate_cq_node.name, generate_og_node.name)
        self._state_graph.add_edge(generate_og_node.name, save_og_node.name)

        self._state_graph.add_edge(save_og_node.name, END)




