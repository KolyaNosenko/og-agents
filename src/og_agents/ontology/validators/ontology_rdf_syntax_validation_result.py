from og_agents.ontology.validators import OntologyValidationResult


class OntologyRDFSyntaxValidationResult(OntologyValidationResult):
    _error: Exception | None

    def __init__(self, error: Exception | None = None):
        super().__init__()
        self._error = error

    def is_valid(self) -> bool:
        return self._error is None

    @property
    def error_message(self) -> str:
        return str(self._error)

    @staticmethod
    def from_error(error: Exception) -> "OntologyRDFSyntaxValidationResult":
        return OntologyRDFSyntaxValidationResult(error)

    @staticmethod
    def success() -> "OntologyRDFSyntaxValidationResult":
        return OntologyRDFSyntaxValidationResult()