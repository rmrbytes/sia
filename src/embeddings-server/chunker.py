# chunker.py

import os
from typing import Dict, Any
from pathlib import Path
from haystack import Pipeline
from haystack.components.writers import DocumentWriter
from haystack.components.converters import (
    MarkdownToDocument,
    PyPDFToDocument,
    TextFileToDocument,
)
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack_integrations.document_stores.chroma import ChromaDocumentStore  # type: ignore
from haystack.document_stores.types import DuplicatePolicy

from config import settings


def chunk_files_in_dir(
    agent_name: str,
    agent_dir: str,
    embedding_model_path: str,
    store_path: str,
    files: Dict[str, Any],
):

    # step 1: clear the store of this agent data
    # ------------------------------------------
    # set the store
    document_store = ChromaDocumentStore(
        collection_name=f"agent_{agent_name}",
        persist_path=store_path,
        distance_function=settings.distance_metric,
    )
    # set the embedder (for step 4)
    document_embedder = SentenceTransformersDocumentEmbedder(model=embedding_model_path)
    document_embedder.warm_up()
    # set the writer (for step 4)
    document_writer = DocumentWriter(
        document_store=document_store, policy=DuplicatePolicy.OVERWRITE
    )
    # delete existing docs if any in the colleciton
    doc_count = document_store.count_documents()
    if doc_count > 0:
        docs = document_store.filter_documents()
        ids = [d.id for d in docs]
        document_store.delete_documents(ids)

    # step 2: create chunking pipeline components
    # -----------------------------------------
    # set the types supported
    file_type_router = FileTypeRouter(
        mime_types=["text/plain", "application/pdf", "text/markdown"]
    )
    # set the converters
    text_file_converter = TextFileToDocument()
    markdown_converter = MarkdownToDocument()
    pdf_converter = PyPDFToDocument()
    # set the cleaner
    document_cleaner = DocumentCleaner()

    # Step 3: loop through the files
    # ------------------------------
    # array to store all split text
    split_docs = []
    for file in files:
        # set the filepath
        file_path = Path(agent_dir) / file["filename"]
        # run the router to get type
        router_res = file_type_router.run(sources=[file_path])
        # array to store all text docs
        txt_docs = []
        # convert to text based on type
        if 'text/plain' in router_res:
            txt_docs = text_file_converter.run(sources=router_res['text/plain'])
        elif 'application/pdf' in router_res:
            txt_docs = pdf_converter.run(sources=router_res['application/pdf'])
        elif 'text/markdown' in router_res:
            txt_docs = markdown_converter.run(sources=router_res['text/markdown'])

        # clean the text
        cleaner_res = document_cleaner.run([txt_docs['documents'][0]])
        # define the splitter based on document meta
        document_splitter = DocumentSplitter(
            split_by=file['meta']['split_by'], 
            split_length=file['meta']['split_length'], 
            split_overlap=file['meta']['split_overlap'], 
            split_threshold=file['meta']['split_threshold']
        )
        # split the cleaned document
        splitter_res = document_splitter.run([cleaner_res['documents'][0]])
        # add the splits to the array
        split_docs.extend(splitter_res['documents'])

    # Step 4: Embed the text_docs & Store it
    # --------------------------------------
    # embedder
    # create the indexing pipeline
    p = Pipeline()
    # add components
    p.add_component(instance=document_embedder, name="embedder")
    p.add_component(instance=document_writer, name="writer")
    # connect them
    p.connect("embedder", "writer")
    p.run({"embedder": {"documents": split_docs}})
    print("done")
    return
