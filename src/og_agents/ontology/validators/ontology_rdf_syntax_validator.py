from rdflib import Graph

from og_agents.ontology.validators.ontology_rdf_syntax_validation_result import OntologyRDFSyntaxValidationResult
from og_agents.ontology.validators.base_ontology_validator import BaseOntologyValidator

class OntologyRDFSyntaxValidator(BaseOntologyValidator):
    def validate_ttl(self, ontology_ttl: str) -> OntologyRDFSyntaxValidationResult:
        try:
            Graph().parse(data=ontology_ttl, format="turtle")
            return OntologyRDFSyntaxValidationResult.success()
        except Exception as error:
            return OntologyRDFSyntaxValidationResult.from_error(error)
