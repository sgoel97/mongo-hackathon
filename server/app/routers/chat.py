from typing import Annotated
from fastapi import APIRouter, Depends
from llama_index import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from openai import OpenAI
import os
import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index.readers.file.base import SimpleDirectoryReader
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.embeddings import TogetherEmbedding
from llama_index.llms import TogetherLLM


# Provide a template following the LLM's original chat template.


router = APIRouter(prefix="/chat", tags=["chat"])


def completion_to_prompt(completion: str) -> str:
    return f"<s>[INST] {completion} [/INST] </s>\n"


@router.post("/")
def run_rag_completion(
    index,
    document_dir: str,
    query_text: str,
    embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
    generative_model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
) -> str:
    # service_context = ServiceContext.from_defaults(
    #     llm=TogetherLLM(
    #         generative_model,
    #         temperature=0.6,
    #         max_tokens=1024,
    #         top_p=0.7,
    #         top_k=50,
    #         # stop=...,
    #         # repetition_penalty=...,
    #         is_chat_model=True,
    #         completion_to_prompt=completion_to_prompt,
    #     ),
    #     embed_model=TogetherEmbedding(embedding_model),
    # )
    # documents = SimpleDirectoryReader(document_dir).load_data()
    # index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    response = index.as_query_engine(similarity_top_k=5).query(query_text)

    return str(response)


@router.post("/rag")
def generate_rag_response(message: str):
    vector_store = vector_store["vector_store"]
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # index = VectorStoreIndex.from_documents(
    #     documents, storage_context=storage_context
    # )

    return {}
