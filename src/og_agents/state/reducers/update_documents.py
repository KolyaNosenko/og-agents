from langchain_core.documents import Document


def update_documents(documents: list[Document], action: list[str]):
    return documents + action
