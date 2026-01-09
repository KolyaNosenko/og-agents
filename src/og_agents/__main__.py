from og_agents.common.http_client import RequestsHttpClient
from og_agents.config import AppConfig
from og_agents.documents import OntologySourceDocument
from og_agents.language_models import OpenAILanguageModel
from og_agents.ontology import OntologyStorage
from og_agents.workflows import OntologyGenerationWorkflowBuilder, WorkflowContext


def main():
    config = AppConfig.init()
    http_client = RequestsHttpClient()

    workflow = OntologyGenerationWorkflowBuilder.create(config).build()
    language_model = OpenAILanguageModel.create(config)
    ontology_storage = OntologyStorage(config)
    # TODO add metadata
    # TODO add structured output
    workflow.invoke(
        {
            'documents': [
                OntologySourceDocument(
                    page_content="""
                        The high status of a classical research University is underpinned by the numerous academic achievements of its staff.
                        The staff at the University have a broad range of formal achievements recognised, in particular with the State Prize of Ukraine in Science and Technology, Awards from the National Academy of Sciences of Ukraine and branches of the national academies of sciences, Orders.
                    """
                ),
            ]
        },
        context=WorkflowContext(
            config=config,
            http_client=http_client,
            language_model=language_model,
            ontology_storage=ontology_storage
        )
    )

if __name__ == "__main__":
    main()