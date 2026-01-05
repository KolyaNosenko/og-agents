from abc import ABC, abstractmethod

from og_agents.ontology.validators.ontology_validation_result import OntologyValidationResult

class BaseOntologyValidator(ABC):
    @abstractmethod
    def validate_ttl(self, ontology_ttl: str) -> OntologyValidationResult:
        pass