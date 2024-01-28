from fastapi import APIRouter, HTTPException, Query, Depends
import together
import pymongo


import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.storage.storage_context import StorageContext
from llama_index.readers.file.base import SimpleDirectoryReader
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.embeddings import TogetherEmbedding
from llama_index.llms import TogetherLLM
from typing import List


# Provide a template following the LLM's original chat template.
def completion_to_prompt(completion: str) -> str:
  return f"<s>[INST] {completion} [/INST] </s>\n"

TOGETHER_API_KEY = "63ab6eb41c340f7eafb146396ccc7bc9051daa395feef9a414204f322af63fcf"
together.api_key = TOGETHER_API_KEY

def generate_embeddings(input_texts: List[str], model_api_string: str) -> List[List[float]]:
    """Generate embeddings from Together python library.

    Args:
        input_texts: a list of string input texts.
        model_api_string: str. An API string for a specific embedding model of your choice.

    Returns:
        embeddings_list: a list of embeddings. Each element corresponds to the each input text.
    """
    together_client = together.Together()
    outputs = together_client.embeddings.create(
        input=input_texts,
        model=model_api_string,
    )
    return [x.embedding for x in outputs.data]



router = APIRouter()
router = APIRouter(prefix="/data", tags=["data"])


@router.post("/resume_add", )
async def try_add_resume_data():

    embedding_model_string = 'togethercomputer/m2-bert-80M-8k-retrieval' # model API string from Together.
    vector_database_field_name = 'embedding_together_m2-bert-8k-retrieval' # define your embedding field name.
    NUM_DOC_LIMIT = 200 # the number of documents you will process and generate embeddings.

    vector_embedding = generate_embeddings(["This is a test."], embedding_model_string)
    print(vector_embedding)

    # documents = SimpleDirectoryReader(
    #     input_files=["/Users/timg/Documents/GitHub/mongo-hackathon/server/TIMOTHY_GUO_RESUME.pdf"]
    # ).load_data()


    mongo_uri = (
        "mongodb+srv://timg51237:01Y4sSZbZxsNFydW@cluster0.qbsk5ke.mongodb.net/?retryWrites=true&w=majority"
    )
    mongodb_client = pymongo.MongoClient(mongo_uri)
    mongodb_db = mongodb_client["beta"]
    mongodb_resumes = mongodb_db["resumes"]
    mongodb_resumes.insert_one({ vector_database_field_name: vector_embedding})


    # store = MongoDBAtlasVectorSearch(mongodb_client)
    # storage_context = StorageContext.from_defaults(vector_store=store)

    # print("Got storage context")
    
    # index = VectorStoreIndex.from_documents(
    #     uber_docs, storage_context=storage_context
    # )

    # print("Loaded into mongo")

    # response = index.as_query_engine().query("What is this document?")

    return { "response": "response"}
    