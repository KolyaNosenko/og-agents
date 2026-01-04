from langchain_core.prompts import PromptTemplate

from src.og_agents.ontology.validators.oops import OOPSValidationResult

PROMPT_TEMPLATE = """
You are an expert in ontology creation and validation.
Your task is to improve the existing ontology based on validation results from the Ontology Pitfall Scanner. Resolve every pitfall listed in the validation result. Detailed explanations for each pitfall are provided below, associated with pitfall numbers like `P08`.

Important:
Return ONLY the final updated RDF, without any additional text.
Bind all resources added to the ontology to the ":" prefix.

# Existing ontology:
{{ ontology }}

# Validation result:
Pitfalls found:
{%- for pitfall in pitfalls %}

{{ pitfall.code }}. {{ pitfall.name }}
Description: {{ pitfall.description }}
Importance: {{ pitfall.importance }}
{%- set affects = pitfall.affects %}
{%- if affects %}
{%- set lines = [] %}
{%- if affects.direct %}{%- set _ = lines.append("- Directly affected resources: " ~ (affects.direct | join(", "))) %}{%- endif %}
{%- if affects.might_be_equivalent_props %}{%- set _ = lines.append("- Might be equivalent properties: " ~ (affects.might_be_equivalent_props | join(", "))) %}{%- endif %}
{%- if affects.might_be_equivalent_attrs %}{%- set _ = lines.append("- Might be equivalent attributes: " ~ (affects.might_be_equivalent_attrs | join(", "))) %}{%- endif %}
{%- if affects.might_not_be_inversed_of %}{%- set _ = lines.append("- Might not be inversed of: " ~ (affects.might_not_be_inversed_of | join(", "))) %}{%- endif %}
{%- if lines %}
Affects:
{{ lines | join("\n") }}
{%- endif %}
{%- endif %}
{%- endfor %}
""".strip()


class OOPSValidationResultPrompt:
    _template: PromptTemplate

    def __init__(self):
        self._template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["pitfalls", "ontology"],
            template_format="jinja2",
        )

    def format(self, ontology_ttl:str, validation_result: OOPSValidationResult) -> str:
        return self._template.format(
            ontology=ontology_ttl,
            pitfalls=validation_result.pitfalls
        )
