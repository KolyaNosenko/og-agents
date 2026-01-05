import os
from langchain_openai import ChatOpenAI
from og_agents.config import AppConfig
from og_agents.language_models.language_model import LanguageModel


class OpenAILanguageModel(LanguageModel, ChatOpenAI):
    @staticmethod
    def create(config: AppConfig):
        if not config.model_provider_api_key:
            raise ValueError("Model provider API key not found")

        if os.environ.get("OPENAI_API_KEY") is None:
            os.environ["OPENAI_API_KEY"] = config.model_provider_api_key

        params = {
            "model": config.language_model_name,
            "service_tier": "flex" if config.app_env == "dev" else None
            # stream_usage=True,
            # temperature=None,
            # max_tokens=None,
            # timeout=None,
            # reasoning_effort="low",
            # max_retries=2,
            # api_key="...", If you prefer to pass api key in directly
            # base_url="...",
            # organization="...",
            # other params...
        }

        return ChatOpenAI(**params)