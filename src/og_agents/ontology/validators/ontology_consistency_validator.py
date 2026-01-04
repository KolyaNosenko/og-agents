from io import BytesIO
from rdflib import Graph
from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError
from src.og_agents.ontology.validators.ontology_consistency_validation_result import OntologyConsistencyValidationResult
from src.og_agents.ontology.validators.base_ontology_validator import BaseOntologyValidator

class OntologyConsistencyValidator(BaseOntologyValidator):
    def validate_ttl(self, ontology_ttl: str) -> OntologyConsistencyValidationResult:
        g = Graph()
        g.parse(data=ontology_ttl, format="turtle")

        rdfxml_bytes = g.serialize(format="xml")
        if isinstance(rdfxml_bytes, str):
            rdfxml_bytes = rdfxml_bytes.encode("utf-8")

        onto = get_ontology("http://www.example.org/test.owl")
        onto.load(fileobj=BytesIO(rdfxml_bytes))

        try:
            sync_reasoner_pellet([onto], infer_property_values=True, debug=2)
            return OntologyConsistencyValidationResult.success()
        except OwlReadyInconsistentOntologyError as e:
            return OntologyConsistencyValidationResult.from_error(e)
