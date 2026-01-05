from abc import ABC

from og_agents.config import AppConfig

class LanguageModel(ABC):
    @staticmethod
    def create(config: AppConfig):
        raise NotImplementedError('Subclasses must implement the create() method')
