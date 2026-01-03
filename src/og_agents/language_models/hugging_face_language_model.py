import os
import torch
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from src.og_agents.language_models.language_model import LanguageModel
from src.og_agents.config import AppConfig

class HuggingFaceLanguageModel(LanguageModel, ChatHuggingFace):
    @staticmethod
    def create(config: AppConfig):
        if not config.model_provider_api_key:
            raise ValueError("Model provider API key not found")

        if os.environ.get("HUGGINGFACEHUB_API_TOKEN") is None:
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = config.model_provider_api_key

        llm = HuggingFacePipeline.from_model_id(
            model_id="INSAIT-Institute/MamayLM-Gemma-3-4B-IT-v1.0",
            task="text-generation",
            pipeline_kwargs=dict(
                do_sample=False,
                repetition_penalty=1.03,
            ),
            model_kwargs=dict(
                dtype=torch.bfloat16,
                attn_implementation="flash_attention_2",
                device_map="auto"
            ),
        )

        return ChatHuggingFace(llm=llm)
