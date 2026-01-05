import streamlit as st
import streamlit.components.v1 as components

from og_agents.config import AppConfig
from og_agents.workflows import OntologyGenerationWorkflowBuilder

st.set_page_config(page_title="", layout="wide")

def render_mermaid(mermaid_code: str, height: int = 800):
    # Mermaid renderer without extra dependencies
    html = f"""
        <div class="mermaid" style="text-align: center;">
            {mermaid_code}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ startOnLoad: true, theme: "default" }});
        </script>
    """
    components.html(html, height=height, scrolling=True)


st.subheader("Візуалізація процесу")

# --- Try to get a mermaid diagram from LangGraph ---
# Depending on your LangGraph version, one of these will exist.
mermaid = None
errors = []

# Option 1 (common): get_graph().draw_mermaid()
config = AppConfig.init()
workflow = OntologyGenerationWorkflowBuilder.create(config).build()

try:
    mermaid = workflow.get_graph().draw_mermaid()
except Exception as e:
    errors.append(f"get_graph().draw_mermaid() failed: {e}")

if mermaid is None:
    try:
        mermaid = workflow.get_graph().to_mermaid()
    except Exception as e:
        errors.append(f"get_graph().to_mermaid() failed: {e}")

if mermaid is None:
    st.error("Could not generate Mermaid from this LangGraph build.")
    st.code("\n".join(errors))
else:
    render_mermaid(mermaid, height=800)


