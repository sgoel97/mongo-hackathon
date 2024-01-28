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
import json
from .data import query_resume_data
import together
from pathlib import Path

# Provide a template following the LLM's original chat template.


router = APIRouter(prefix="/chat", tags=["chat"])


def completion_to_prompt(completion: str) -> str:
    return f"<s>[INST] {completion} [/INST] </s>\n"


@router.post("/")
def run_rag_completion(
    # index,
    # document_dir: str,
    query_text: str,
    embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
    generative_model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
):

    vector_responses = query_resume_data(query_text)["response"]
    augmented_query = "Context </s>"
    for data in vector_responses:
        augmented_query += data["text"]
        augmented_query += "</s>"
    augmented_query += (
        "Answer the following query. Do not mention that you used the context provided previously."
        + "</s>"
        + query_text
    )
    print(augmented_query)
    response_chocies = together.Complete.create(
        prompt=augmented_query,
        model=generative_model,
        max_tokens=512,
        temperature=0.6,
        top_k=60,
        top_p=0.6,
        repetition_penalty=1.1,
    )

    response = response_chocies["output"]["choices"][0]["text"]  # str(response)

    with open("./app/db/messages/message_history.json", "r") as f:
        curr_messages = json.load(f)

    curr_messages["messages"].append({"role": "user", "message": query_text})
    curr_messages["messages"].append({"role": "assistant", "message": response})

    with open("./app/db/messages/message_history.json", "w") as f:
        json.dump(curr_messages, f)

    return {"response": response, "files": [x["file_name"] for x in vector_responses]}


@router.get("/demo")
def get_demo(
    query_text,
    generative_model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
):
    path = Path("./app/db/files")
    path.mkdir(parents=True, exist_ok=True)
    file_names = list(path.glob("*.pdf"))
    file_names = [x.name for x in file_names]
    file_names = " ".join(file_names)

    query_text = f"""
    here are some resume filenames:

    {file_names}

    please answer my question:

    {query_text}
    """
    response_chocies = together.Complete.create(
        prompt=query_text,
        model=generative_model,
        max_tokens=512,
        temperature=0.6,
        top_k=60,
        top_p=0.6,
        repetition_penalty=1.1,
    )
    response = response_chocies["output"]["choices"][0]["text"]  # str(response)
    return str(response)
