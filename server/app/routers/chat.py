from typing import Annotated
from fastapi import APIRouter, Depends, Security
from llama_index import VectorStoreIndex
from ..dependencies import get_vector_database
from llama_index.storage.storage_context import StorageContext
from ..utils import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.post("/chat/message")
async def on_message(message: str, auth_result: str = Security(auth.verify)):
    print(auth_result)
    import random
    random_case = lambda ch: ch.lower() if random.random() < 0.5 else ch.upper()
    response = ''.join(map(random_case, message))
    return {'response': response}

@router.post("/chat/rag")
def generate_rag_response(message: str, vector_store: Annotated[dict, Depends(get_vector_database)]):
    vector_store = vector_store["vector_store"]
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # index = VectorStoreIndex.from_documents(
    #     documents, storage_context=storage_context
    # )
