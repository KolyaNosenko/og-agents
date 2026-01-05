import streamlit as st
from dataclasses import dataclass
from langgraph.graph.state import CompiledStateGraph
from rdflib import Graph
import streamlit.components.v1 as components

from og_agents.config import AppConfig
from og_agents.documents import OntologySourceDocument
from og_agents.common.http_client import RequestsHttpClient
from og_agents.ontology.ontology_storage import OntologyStorage
from og_agents.workflows import OntologyGenerationWorkflowBuilder, WorkflowContext
from og_agents.workflows.nodes import (
    GENERATE_COMPETENCY_QUESTIONS_NODE_NAME,
    GENERATE_ONTOLOGY_NODE_NAME,
    ONTOLOGY_CONSISTENCY_VALIDATION_NODE_NAME,
    ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME,
    OOPS_ONTOLOGY_VALIDATION_NODE_NAME,
)
from og_agents.workflows.requests import GenerateOntologyRequest
from og_agents.language_models import OpenAILanguageModel
from og_agents.state import GenerationState
from og_agents.app.ontology_visualization import visualize_ontology

@dataclass(frozen=True)
class AppDependencies:
    app_config: AppConfig
    ontology_storage: OntologyStorage
    http_client: RequestsHttpClient
    language_model: OpenAILanguageModel
    ontology_generation_workflow: CompiledStateGraph[GenerationState, WorkflowContext, GenerateOntologyRequest]

@st.cache_resource
def init_app_dependencies() -> AppDependencies:
    app_config = AppConfig.init()
    storage = OntologyStorage(app_config)
    http_client = RequestsHttpClient()
    language_model = OpenAILanguageModel.create(app_config)

    og_generation_workflow = OntologyGenerationWorkflowBuilder.create(app_config).build()

    return AppDependencies(
        app_config=app_config,
        ontology_storage=storage,
        http_client=http_client,
        language_model=language_model,
        ontology_generation_workflow=og_generation_workflow,
    )

st.set_page_config(layout="wide")

app_dependencies = init_app_dependencies()
ontology_storage = app_dependencies.ontology_storage
ontology_generation_workflow = app_dependencies.ontology_generation_workflow

if "is_ontology_exists" not in st.session_state:
    st.session_state.is_ontology_exists = False

INITIAL_LIMIT = 1000

try:
    is_ontology_exists = ontology_storage.is_exist()
    st.session_state.is_ontology_exists = is_ontology_exists
except Exception as e:
    st.error(f"Помилка завантаження онтології: {e}")

if not st.session_state.is_ontology_exists:
    st.title('Онтологію не знайдено, створіть нову')

    uploaded_file = st.file_uploader(
        "Додати файл",
        type=["txt"],
    )

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8", errors="ignore")

        st.header('Створення онтології з тексту:')
        st.caption(text)

        workflow_execution = st.container()
        last_step = None

        # TODO add metadata
        # TODO add structured output
        for chunk in ontology_generation_workflow.stream(
            {
                'documents': [
                    OntologySourceDocument(page_content=text),
                ]
            },
            context=WorkflowContext(
                config=app_dependencies.app_config,
                http_client=app_dependencies.http_client,
                language_model=app_dependencies.language_model,
                ontology_storage=app_dependencies.ontology_storage
            ),
            stream_mode="custom",
        ):
            with workflow_execution:
                if 'current_step' not in chunk:
                    continue

                if not last_step:
                    st.subheader(f'Поточний крок {chunk['current_step']}', divider=True)
                    last_step = chunk['current_step']
                elif last_step != chunk['current_step']:
                    st.subheader(f'Поточний крок {chunk['current_step']}', divider=True)
                    last_step = chunk['current_step']

                if chunk['current_step'] == GENERATE_COMPETENCY_QUESTIONS_NODE_NAME:
                    if 'competency_questions' in chunk:
                        st.write(chunk['message'])
                        st.code(chunk['competency_questions'])
                    else:
                        st.write(chunk['message'])
                elif chunk['current_step'] == GENERATE_ONTOLOGY_NODE_NAME:
                    if 'ontology_ttl' in chunk:
                        st.write(chunk['message'])
                        st.code(chunk['ontology_ttl'])
                    else:
                        st.write(chunk['message'])
                elif chunk['current_step'] == ONTOLOGY_RDF_SYNTAX_VALIDATION_NODE_NAME:
                    if 'error' in chunk:
                        st.write(chunk['message'])
                        st.warning(chunk['error'])
                    elif 'ontology_ttl' in chunk:
                        st.write(chunk['message'])
                        st.code(chunk['ontology_ttl'])
                    else:
                        st.write(chunk['message'])
                elif chunk['current_step'] == OOPS_ONTOLOGY_VALIDATION_NODE_NAME:
                    if 'error' in chunk:
                        st.write(chunk['message'])
                        st.warning(chunk['error'])
                    elif 'ontology_ttl' in chunk:
                        st.write(chunk['message'])
                        st.code(chunk['ontology_ttl'])
                    else:
                        st.write(chunk['message'])
                elif chunk['current_step'] == ONTOLOGY_CONSISTENCY_VALIDATION_NODE_NAME:
                    if 'error' in chunk:
                        st.write(chunk['message'])
                        st.warning(chunk['error'])
                    elif 'ontology_ttl' in chunk:
                        st.write(chunk['message'])
                        st.code(chunk['ontology_ttl'])
                    else:
                        st.write(chunk['message'])
                else:
                    st.write(chunk['message'])
        else:
            with workflow_execution:
                st.success('Онтологію створено!')
                st.divider()
                st.balloons()
                show = st.button("🚀 Показати онтологію")

                if show:
                    st.session_state.is_ontology_exists = True
                    st.rerun()

@st.dialog("RDF (Turtle)")
def rdf_modal(rdf_graph: Graph):
    ttl_text = rdf_graph.serialize(format="turtle")

    st.download_button(
        "⬇️ Завантажити ontology.ttl",
        data=ttl_text,
        file_name="ontology.ttl",
        mime="text/turtle",
        use_container_width=True,
    )
    st.code(ttl_text, language="turtle")

if st.session_state.is_ontology_exists:
    st.title("Онтологія")

    with st.sidebar:
        st.header("Налаштування графа")

        height = st.slider("Висота (px)", 200, 2000, 700, 50)
        limit = st.slider("Макс. кількість зв'язків", 10, 2000, INITIAL_LIMIT, 10)

        initial_zoom = st.slider("Початковий зум", 0.1, 1.0, 0.8, 0.1)

        st.divider()

        show_schema_only = st.checkbox("📐 Тільки схема (OWL/RDFS)", value=False)
        show_classes = st.checkbox("Класи", True)
        show_object_props = st.checkbox("Object Properties", True)
        show_data_props = st.checkbox("Datatype Properties", True)
        show_individuals = st.checkbox("Індивіди", True)

        st.divider()

        show_labels = st.checkbox("🏷 Показувати назви", False)
        show_comments = st.checkbox("💬 Показувати коментарі", False)
        physics = st.checkbox("🧲 Physics (layout)", True)

        st.divider()

        reset = st.button("🧨 Видалити Онтологію")

        if reset:
            ontology_storage.destroy()

            st.cache_data.clear()

            st.success("Онтологію видалено")
            st.session_state.is_ontology_exists = False
            st.rerun()

    try:
        rdf_graph: Graph = ontology_storage.get_world_as_rdf_graph()

        show_rdf = st.button("📄 Показати RDF (Turtle)")

        if show_rdf:
            rdf_modal(rdf_graph)

        net = visualize_ontology(
            rdf_graph,
            height=height,
            limit=limit,
            show_classes=show_classes,
            show_object_props=show_object_props,
            show_data_props=show_data_props,
            show_individuals=show_individuals,
            show_schema_only=show_schema_only,
            show_labels=show_labels,
            show_comments=show_comments,
            physics=physics,
            initial_zoom=initial_zoom,
        )

        html = net.generate_html()
        components.html(html, height=height + 50, scrolling=True)
    except Exception as e:
        st.error(f"Помилка завантаження графа: {e}")

