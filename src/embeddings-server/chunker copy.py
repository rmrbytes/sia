# chunker.py

import os
from pathlib import Path
from haystack import Pipeline
from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack.document_stores.types import DuplicatePolicy

#from haystack.document_stores.types import DuplicatePolicy

from config import settings

def chunk_files_in_dir(agent_name:str, dir: str, model_path: str, store_path: str):
    # set the types supported
    file_type_router = FileTypeRouter(mime_types=["text/plain", "application/pdf", "text/markdown"])

    # set the converters
    text_file_converter = TextFileToDocument()
    markdown_converter = MarkdownToDocument()
    pdf_converter = PyPDFToDocument()

    # set the cleaner and splitter
    document_cleaner = DocumentCleaner()
    document_splitter = DocumentSplitter(
        split_by=settings.chunk_strategy, 
        split_length=settings.chunk_size, 
        split_overlap=settings.chunk_overlap,
        split_threshold=settings.min_chunk_size)

    # set the joiner
    document_joiner = DocumentJoiner()

    # set the embedder
    document_embedder = SentenceTransformersDocumentEmbedder(model=model_path)

    # set the store
    document_store = ChromaDocumentStore(collection_name=f"agent_{agent_name}", persist_path=store_path, distance_function=settings.distance_metric)
    document_writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.OVERWRITE)

    # delete existing docs if any in the colleciton
    doc_count = document_store.count_documents()
    if doc_count > 0:
        docs = document_store.filter_documents()
        ids = [d.id for d in docs]
        document_store.delete_documents(ids)

    # add components to the pipeline
    preprocessing_pipeline = Pipeline()
    # router
    preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
    # document converters
    preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
    preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
    preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
    # joiner
    preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
    # cleaner
    preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
    # splitter
    preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
    # embedder
    preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
    # document writer
    preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

    # connect the router with sources
    preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
    preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
    preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")

    # connect components with document joiner
    preprocessing_pipeline.connect("text_file_converter", "document_joiner")
    preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
    preprocessing_pipeline.connect("markdown_converter", "document_joiner")

    # connect the document joiner with cleaner
    preprocessing_pipeline.connect("document_joiner", "document_cleaner")
    # connect cleaner with splitter
    preprocessing_pipeline.connect("document_cleaner", "document_splitter")
    # connect splitter with embedder
    preprocessing_pipeline.connect("document_splitter", "document_embedder")
    preprocessing_pipeline.connect("document_embedder", "document_writer")

    # run the pipeline
    result = preprocessing_pipeline.run({"file_type_router": {"sources": list(Path(dir).glob("**/*"))}})
    return
