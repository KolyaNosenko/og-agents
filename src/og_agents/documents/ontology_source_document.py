from langchain_core.documents import Document

DOC_DELIMITER = "\n--- DOCUMENT {i} ---\n"

class OntologySourceDocument(Document):
    def to_prompt_format(self, doc_index: int | None = None):
        return DOC_DELIMITER.format(i=doc_index) + self.page_content.strip()


    #   FOR REASONING FORMAT
    # def to_prompt(self):
    #     for i, doc in enumerate(documents, start=1):
    #         source = doc.metadata.get("source", "unknown")
    #         title = doc.metadata.get("title", "untitled")
    #
    #         formatted_documents.append(
    #             f"""<document id="{i}">
    #       <metadata>
    #         <source>{source}</source>
    #         <title>{title}</title>
    #       </metadata>
    #       <content>
    #     {doc.page_content.strip()}
    #       </content>
    #     </document>