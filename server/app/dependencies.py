from typing import Annotated

from fastapi import Header, HTTPException, Depends

import weaviate
from llama_index import VectorStoreIndex
from llama_index.vector_stores import WeaviateVectorStore
from .constants import VectorStoreProvider

# TODO: use some middleware to figure this out.
async def get_current_user():
    return { "vector_database_provider": VectorStoreProvider.WEAVIATE }

## Eventually figure out which vector DB to get

async def get_vector_database(user: Annotated[dict, Depends(get_current_user)]):
    if user["vector_database_provider"] == VectorStoreProvider.WEAVIATE:
        return get_weaviate_database("https://shattuck-street-research-mvp-y3wii635.weaviate.network", "iMnbikyN1Ac3ip3X3WcZWLh8RU2kYwMgzeFX", "LlamaIndex")

# TODO: Differentiate between conencting to a user's weaviate and our own weaviate
def get_weaviate_database(url: str, api_key: str, index_name):
    client = weaviate.Client(
        url=url,
        auth_client_secret=weaviate.AuthApiKey(api_key=api_key)
    )

    vector_store = WeaviateVectorStore(
        weaviate_client=client, index_name=index_name
    )

    return {"vector_store": vector_store}
