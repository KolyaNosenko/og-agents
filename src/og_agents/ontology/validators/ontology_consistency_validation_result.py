from src.og_agents.ontology.validators.ontology_validation_result import OntologyValidationResult

class OntologyConsistencyValidationResult(OntologyValidationResult):
    _error: None | Exception

    def __init__(self, error: None | Exception = None):
        super().__init__()
        self._error = error

    def is_valid(self) -> bool:
        return self._error is None

    @property
    def error_message(self) -> str:
        return str(self._error)

    @staticmethod
    def from_error(error: Exception) -> "OntologyConsistencyValidationResult":
        return OntologyConsistencyValidationResult(error)

    @staticmethod
    def success() -> "OntologyConsistencyValidationResult":
        return OntologyConsistencyValidationResult()


