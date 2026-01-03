from abc import ABC, abstractmethod

from src.og_agents.config import AppConfig

class EmbeddingsModel(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        pass

    @staticmethod
    def create(config: AppConfig):
        raise NotImplementedError('Subclasses must implement the create() method')
