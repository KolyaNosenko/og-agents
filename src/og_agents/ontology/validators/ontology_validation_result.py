from abc import ABC, abstractmethod

class OntologyValidationResult(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        pass
