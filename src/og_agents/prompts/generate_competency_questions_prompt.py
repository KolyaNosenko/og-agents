from langchain_core.prompts import PromptTemplate

from og_agents.documents import OntologySourceDocument

# PROMPT_TEMPLATE = """
# You are an expert in Specification and Knowledge Representation.
# Your purpose is to develop competency questions for ontology.
# Competency questions are a natural language question that specifies the requirements of an ontology and can be answered by that ontology.
# Derive competency questions, using the provided documents.
#
# Documents: {documents}
#
# Return ONLY the competency questions, no other text.
# """

# PROMPT_TEMPLATE = """
# You are an expert in Specification and Knowledge Representation.
# Your purpose is to develop competency questions for ontology.
# Competency questions are a natural language question that specifies the requirements of an ontology and can be answered by that ontology.
# Derive competency questions, using the provided documents.
#
# Documents: {documents}
#
# Return ONLY the competency questions, no other text.
# """
# TODO add normal few shot prompting
PROMPT_TEMPLATE = """
Ти є експертом зі специфікації та представлення знань.
Твоя мета — розробити питання компетентності для еталонної онтології.
Питання компетентності — це питання природною мовою, які задають вимоги до онтології та на які ця онтологія повинна вміти відповідати.
Сформулюй питання компетентності, використовуючи надані документи.

Документи: {documents}

Поверни **ЛИШЕ** питання компетентності, без будь-якого іншого тексту.
"""

class GenerateCompetencyQuestionsPrompt:
    _template: PromptTemplate

    def __init__(self):
        self._template = PromptTemplate.from_template(PROMPT_TEMPLATE)

    def format(self, documents: list[OntologySourceDocument]) -> str:
        formatted_documents = []

        for index, document in enumerate(documents):
            formatted_documents.append(document.to_prompt_format(index))

        joined_documents = '\n'.join(formatted_documents)

        return self._template.format(documents=joined_documents)