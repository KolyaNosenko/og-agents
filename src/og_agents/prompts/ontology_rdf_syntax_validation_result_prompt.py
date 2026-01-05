from langchain_core.prompts import PromptTemplate

from src.og_agents.ontology.validators import OntologyRDFSyntaxValidationResult

PROMPT_TEMPLATE = """
You are an expert in ontology creation and validation.
Your task is to fix the existing ontology based on validation results from RDF Turtle syntax validator and provide strictly valid RDF Turtle Ontology as a result.
Resolve every RDF Turtle syntax problem in provided ontology.

Important:
Return ONLY the final fixed RDF, without any additional text.
Bind all ontology resources to the ":" prefix.

# Existing ontology:
{ontology}

# RDF Turtle syntax validation result:
{error_message}
""".strip()


class OntologyRDFSyntaxValidationResultPrompt:
    _template: PromptTemplate

    _template: PromptTemplate

    def __init__(self):
        self._template = PromptTemplate.from_template(PROMPT_TEMPLATE)

    def format(
            self,
            ontology_ttl: str,
            validation_result: OntologyRDFSyntaxValidationResult
    ) -> str:
        return self._template.format(
            ontology=ontology_ttl,
            error_message=validation_result.error_message
        )
