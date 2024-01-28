from typing import Annotated
from fastapi import APIRouter, Depends, Security
from llama_index import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def on_message(message: str):
    import random

    random_case = lambda ch: ch.lower() if random.random() < 0.5 else ch.upper()
    response = "".join(map(random_case, message))
    return {"response": response}


@router.post("/rag")
def generate_rag_response(
    message: str
):
    vector_store = vector_store["vector_store"]
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # index = VectorStoreIndex.from_documents(
    #     documents, storage_context=storage_context
    # )

    return {}