from langchain_core.prompts import PromptTemplate

from og_agents.ontology.validators import OntologyRDFSyntaxValidationResult

# PROMPT_TEMPLATE = """
# You are an expert in ontology creation and validation.
# Your task is to fix the existing ontology based on validation results from RDF Turtle syntax validator and provide strictly valid RDF Turtle Ontology as a result.
# Resolve every RDF Turtle syntax problem in provided ontology.
#
# Important:
# Return ONLY the final fixed RDF, without any additional text.
# Bind all ontology resources to the ":" prefix.
#
# # Existing ontology:
# {ontology}
#
# # RDF Turtle syntax validation result:
# {error_message}
# """.strip()

PROMPT_TEMPLATE = """
Ти є експертом зі створення та валідації онтологій.
Твоє завдання — виправити наявну онтологію на основі результатів валідатора синтаксису RDF Turtle та надати в результаті коректну онтологію у форматі RDF Turtle.
Виправ кожну синтаксичну помилку RDF Turtle у наданій онтології.

Важливо:
1. Поверни ЛИШЕ фінальний виправлений RDF, без будь-якого іншого тексту.
2. Прив’яжи усі ресурси, що додаються до онтології, до префікса ":".

# Наявна онтологія:
{ontology}

# Результат перевірки синтаксису RDF Turtle:
{error_message}
"""


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
