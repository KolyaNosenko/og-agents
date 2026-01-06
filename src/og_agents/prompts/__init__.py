from og_agents.prompts.generate_competency_questions_prompt import GenerateCompetencyQuestionsPrompt
from og_agents.prompts.generate_ontology_prompt import GenerateOntologyPrompt
from og_agents.prompts.oops_validation_result_prompt import OOPSValidationResultPrompt
from og_agents.prompts.ontology_consistency_validation_result_prompt import OntologyConsistencyValidationResultPrompt
from og_agents.prompts.ontology_rdf_syntax_validation_result_prompt import OntologyRDFSyntaxValidationResultPrompt
from og_agents.prompts.sparql_prompts import SPARQL_GENERATION_SELECT_PROMPT, SPARQL_GENERATION_UPDATE_PROMPT

__all__ = [
    "GenerateCompetencyQuestionsPrompt",
    "GenerateOntologyPrompt",
    "OOPSValidationResultPrompt",
    "OntologyConsistencyValidationResultPrompt",
    "OntologyRDFSyntaxValidationResultPrompt",
    "SPARQL_GENERATION_SELECT_PROMPT",
    "SPARQL_GENERATION_UPDATE_PROMPT",
]
