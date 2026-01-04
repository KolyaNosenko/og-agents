from rdflib import Graph

from src.og_agents.ontology.validators import OntologyValidationResult
from src.og_agents.ontology.validators.base_ontology_validator import BaseOntologyValidator

class RDFOntologyValidator(BaseOntologyValidator):
    def validate_ttl(self, ontology_ttl: str) -> OntologyValidationResult:
        try:
            Graph().parse(data=ontology_ttl, format="turtle")
            return OntologyValidationResult.success()
        except Exception as error:
            return OntologyValidationResult.from_error(error)
