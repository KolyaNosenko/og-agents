import streamlit as st
from dataclasses import dataclass
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph
from langchain_community.graphs import RdfGraph
from langchain_community.chains.graph_qa.sparql import GraphSparqlQAChain

from og_agents.config import AppConfig
from og_agents.common.http_client import RequestsHttpClient
from og_agents.workflows import OntologyGenerationWorkflowBuilder, WorkflowContext
from og_agents.workflows.requests import GenerateOntologyRequest
from og_agents.language_models import OpenAILanguageModel
from og_agents.state import GenerationState
from og_agents.prompts import SPARQL_GENERATION_SELECT_PROMPT, SPARQL_GENERATION_UPDATE_PROMPT

from rdflib.namespace import RDF, OWL, RDFS
from rdflib import Graph

def is_ontology_exist(graph: Graph) -> bool:
    return any(graph.triples((None, RDF.type, OWL.Class))) or \
           any(graph.triples((None, RDF.type, OWL.ObjectProperty))) or \
           any(graph.triples((None, RDF.type, OWL.DatatypeProperty))) or \
           any(graph.triples((None, RDF.type, RDFS.Class)))

st.set_page_config(page_title="Чат", layout="centered")

st.title("Що хочеш дізнатися?")

@dataclass(frozen=True)
class AppDependencies:
    app_config: AppConfig
    http_client: RequestsHttpClient
    language_model: OpenAILanguageModel
    ontology_generation_workflow: CompiledStateGraph[GenerationState, WorkflowContext, GenerateOntologyRequest]


@st.cache_resource
def init_app_dependencies() -> AppDependencies:
    app_config = AppConfig.init()
    http_client = RequestsHttpClient()
    language_model = OpenAILanguageModel.create(app_config)
    og_generation_workflow = OntologyGenerationWorkflowBuilder.create(app_config).build()

    return AppDependencies(
        app_config=app_config,
        http_client=http_client,
        language_model=language_model,
        ontology_generation_workflow=og_generation_workflow,
    )


app_dependencies = init_app_dependencies()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_ontology_exists" not in st.session_state:
    st.session_state.is_ontology_exists = False

try:
    ttl_path = Path(app_dependencies.app_config.db.tutle_fallback_path)

    if ttl_path.exists():
        rdf_graph = Graph().parse(app_dependencies.app_config.db.tutle_fallback_path, format="turtle")
        st.session_state.is_ontology_exists = is_ontology_exist(rdf_graph)
    else:
        st.session_state.is_ontology_exists = False
except Exception as e:
    st.error(f"Помилка завантаження онтології: {e}")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("content"):
            st.markdown(msg["content"])
            if msg.get('sparql_query'):
                st.caption('Використано SPARQL:')
                st.code(msg["sparql_query"], language="sparql")


if not st.session_state.is_ontology_exists:
    st.warning("Онтологія не знайдена. Спочатку згенеруйте або завантажте її.")
    st.stop()

graph = RdfGraph(
    source_file=app_dependencies.app_config.db.tutle_fallback_path,
    standard="owl",
)
graph.load_schema()

chain = GraphSparqlQAChain.from_llm(
    llm=app_dependencies.language_model,
    graph=graph,
    verbose=True,
    sparql_select_prompt= SPARQL_GENERATION_SELECT_PROMPT,
    sparql_update_prompt= SPARQL_GENERATION_UPDATE_PROMPT,
    return_sparql_query=True,
    allow_dangerous_requests=True,
)

prompt = st.chat_input("Ставте запитання")

if prompt:
    # 1) Save + display user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) Run chain + display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                result = chain.invoke({"query": prompt})
                answer_text = (result or {}).get("result", "")
                sparql_query = (result or {}).get("sparql_query", "")

                # Show answer
                st.markdown(answer_text if answer_text else "_(порожня відповідь)_")
                st.caption('Використано SPARQL:')
                st.code(sparql_query, language="sparql")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer_text,
                        "sparql_query": sparql_query,
                    }
                )

            except Exception as e:
                st.error(f"Помилка виконання запиту: {e}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"❌ Помилка: {e}"}
                )