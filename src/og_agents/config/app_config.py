import os
from dotenv import load_dotenv

class AppConfig:
    _app_env: str
    _model_provider_api_key: str
    _language_model_name: str
    _embeddings_model_name: str

    def __init__(self):
        self._app_env = os.getenv('APP_ENV', 'dev')
        self._model_provider_api_key = os.getenv('MODEL_PROVIDER_API_KEY')
        self._language_model_name = os.getenv('LANGUAGE_MODEL_NAME')
        self._embeddings_model_name = os.getenv('EMBEDDINGS_MODEL_NAME')

    @property
    def model_provider_api_key(self):
        return self._model_provider_api_key

    @property
    def language_model_name(self):
        return self._language_model_name

    @property
    def embeddings_model_name(self):
        return self._embeddings_model_name

    @property
    def app_env(self):
        return self._app_env

    # TODO add validation
    def _validate(self):
        return True

    @staticmethod
    def init() -> 'AppConfig':
        load_dotenv()
        config = AppConfig()
        config._validate()

        return AppConfig()
