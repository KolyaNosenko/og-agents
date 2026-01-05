from langchain_core.prompts import PromptTemplate

from og_agents.ontology.validators import OntologyConsistencyValidationResult

# PROMPT_TEMPLATE = """
# You are an expert in ontology creation and validation.
# Your task is to fix the existing ontology based on validation results from reasoner.
# Resolve every problems in provided ontology that reasoner provided.
#
# Important:
# Return ONLY the final fixed RDF, without any additional text.
# Bind all ontology resources to the ":" prefix.
#
# # Existing ontology:
# {ontology}
#
# # Reasoner validation result:
# {error_message}
# """.strip()

PROMPT_TEMPLATE = """
Ти є експертом зі створення та валідації онтологій.
Твоє завдання — виправити наявну онтологію на основі результатів валідації, отриманих після формальної перевірки.
Виправ всі проблеми в наданій онтології, які виявлено після формальної перевірки.

Важливо:
1. Поверни ЛИШЕ фінальний виправлений RDF, без будь-якого іншого тексту.
2. Прив’яжи усі ресурси, що додаються до онтології, до префікса ":".

# Наявна онтологія:
{ontology}

# Результат формальної перевірки:
{error_message}
""".strip()


class OntologyConsistencyValidationResultPrompt:
    _template: PromptTemplate

    _template: PromptTemplate

    def __init__(self):
        self._template = PromptTemplate.from_template(PROMPT_TEMPLATE)

    def format(
            self,
            ontology_ttl: str,
            validation_result: OntologyConsistencyValidationResult
    ) -> str:
        return self._template.format(
            ontology=ontology_ttl,
            error_message=validation_result.error_message
        )
