from fastapi import APIRouter
import together
import pymongo
from typing import List

router = APIRouter()
router = APIRouter(prefix="/data", tags=["data"])



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




@router.post("/resume_add", )
async def try_add_resume_data(text: str):

    embedding_model_string = 'togethercomputer/m2-bert-80M-8k-retrieval' # model API string from Together.
    vector_database_field_name = 'embedding_together_m2-bert-8k-retrieval' # define your embedding field name.
    NUM_DOC_LIMIT = 200 # the number of documents you will process and generate embeddings.

    vector_embedding = generate_embeddings([text], embedding_model_string)

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

    return { "response": "response"}
    