# delete.py

from haystack_integrations.document_stores.chroma import ChromaDocumentStore  # type: ignore

from config import settings


def delete_agent_embeddings(
    agent_name: str,
    store_path: str
):

    # set the store
    document_store = ChromaDocumentStore(
        collection_name=f"agent_{agent_name}",
        persist_path=store_path
    )
    # delete existing docs if any in the collection
    doc_count = document_store.count_documents()
    if doc_count > 0:
        docs = document_store.filter_documents()
        ids = [d.id for d in docs]
        document_store.delete_documents(ids)

    return
