import os
from typing import Any
from langchain_openai import OpenAIEmbeddings
from src.og_agents.config import AppConfig
from src.og_agents.embeddings.embeddings_model import EmbeddingsModel

class OpenAIEmbeddingsModel(EmbeddingsModel):
    _open_ai_embeddings: OpenAIEmbeddings

    def __init__(self, config: AppConfig):
        self._open_ai_embeddings = OpenAIEmbeddings(model=config.embeddings_model_name)

    @staticmethod
    def create(config: AppConfig):
        if not config.model_provider_api_key:
            raise ValueError("Model provider API key not found")

        if os.environ.get("OPENAI_API_KEY") is None:
            os.environ["OPENAI_API_KEY"] = config.model_provider_api_key

        return OpenAIEmbeddingsModel(config)

    # TODO use documents from langchain
    def embed_documents(
            self, texts: list[str], chunk_size: int | None = None, **kwargs: Any
    ) -> list[list[float]]:
        return self._open_ai_embeddings.embed_documents(
            texts,
            chunk_size=chunk_size,
            **kwargs
        )

    def embed_query(self, text: str, **kwargs: Any) -> list[float]:
        return self._open_ai_embeddings.embed_query(text, **kwargs)
