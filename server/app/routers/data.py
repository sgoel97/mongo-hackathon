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

import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index.readers.file.base import SimpleDirectoryReader

router = APIRouter()
router = APIRouter(prefix="/data", tags=["data"])


@router.post("/resume_try", )
async def try_read_resume_data():
    mongo_uri = (
        "mongodb+srv://timg51237:01Y4sSZbZxsNFydW@cluster0.qbsk5ke.mongodb.net/?retryWrites=true&w=majority"
    )

    mongodb_client = pymongo.MongoClient(mongo_uri)
    store = MongoDBAtlasVectorSearch(mongodb_client)
    storage_context = StorageContext.from_defaults(vector_store=store)

    print("Got storage context")
    uber_docs = SimpleDirectoryReader(
        input_files=["/Users/timg/Documents/GitHub/mongo-hackathon/server/TIMOTHY_GUO_RESUME.pdf"]
    ).load_data()
    index = VectorStoreIndex.from_documents(
        uber_docs, storage_context=storage_context
    )

    print("Loaded into mongo")

    response = index.as_query_engine().query("What is this document?")

    return { response: "response"}
    