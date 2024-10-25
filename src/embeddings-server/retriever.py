# chunker.py

import os
from pathlib import Path
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever

from config import settings

def get_chunks(agent_name:str, prompt: str, embedding_model_path: str, store_path: str):

    # set the embedder
    text_embedder = SentenceTransformersTextEmbedder(model=embedding_model_path)
    # set the store
    document_store = ChromaDocumentStore(collection_name=f"agent_{agent_name}", persist_path=store_path, distance_function=settings.distance_metric)
    # set the retriever for the store
    retriever = ChromaEmbeddingRetriever(document_store=document_store, top_k=settings.top_n)

    # add components to the pipeline
    q = Pipeline()
    # embedder
    q.add_component("query_embedder", text_embedder)
    q.add_component("retriever", retriever)
    q.connect("query_embedder.embedding", "retriever.query_embedding")
    results = q.run({"query_embedder": {"text": prompt}})
    chunks = []
    for d in results["retriever"]["documents"]:
        chunks.append(d.content.replace('\n', ' '))
    return chunks
