import weaviate
from fastapi import APIRouter, HTTPException, Query, Depends
from llama_index import (SimpleDirectoryReader, VectorStoreIndex,
                         download_loader)
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.text_splitter import SentenceSplitter
from llama_index.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache,
)
from llama_index import Document
from typing import Annotated

from utils.GoogleDriveReader import GoogleDriveReader
from llama_index.readers import WikipediaReader
from ..dependencies import get_vector_database

router = APIRouter()


@router.get("/data/drive_try", )
async def try_read_google_drive_data():
    loader = GoogleDriveReader()

    #### Using file id
    documents = loader.load_data(file_ids=["1lM9IpuvOPGg3xs_TqxEZkmDKu3U5Vfp1txipa11_fag"])

    return { "documents": documents}

def process_google_drive_document(document):
    document.id_ = document.metadata["file_name"]
    return document

@router.post("/data/drive/", )
async def load_google_drive_data(
    access_token: Annotated[str, Query()],
    vector_store: Annotated[dict, Depends(get_vector_database)],
    folder_ids: Annotated[list[str], Query()] = None,
    file_ids: Annotated[list[str], Query()] = None
):
    loader = GoogleDriveReader()

    print(file_ids)
    
    documents_raw = loader.load_data(
        folder_ids=folder_ids,
        file_ids=file_ids,
        access_token=access_token
    )

    if not documents_raw:
        raise HTTPException(status_code=400, detail="No valid documents found")
    
    print(documents_raw)
    
    documents = list(map(process_google_drive_document, documents_raw))
    print(documents)

    vector_store = vector_store.get("vector_store")

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(),
            embed_model,
        ],
        vector_store=vector_store,
    )
    nodes = pipeline.run(documents=documents)
    print(f"Ingested {len(nodes)} Nodes")

    # index = VectorStoreIndex.from_vector_store(vector_store)

    return { "success": True, "nodes": len(nodes) }

@router.post("/data/wikipedia")
def load_wikipedia_data(pages: Annotated[list[str], Query()],    vector_store: Annotated[dict, Depends(get_vector_database)]):
    loader = WikipediaReader()
    documents = loader.load_data(pages=pages)

    vector_store = vector_store.get("vector_store")

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(),
            embed_model,
        ],
        vector_store=vector_store,
    )
    nodes = pipeline.run(documents=documents)
    print(f"Ingested {len(nodes)} Nodes")

    return { "success": True, "documents": documents}

