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

@router.post("/query")
async def try_query_resume_data(query: str):

    embedding_model_string = 'togethercomputer/m2-bert-80M-8k-retrieval' # model API string from Together.
    vector_database_field_name = 'embedding_together_m2-bert-8k-retrieval' # define your embedding field name.
    vector_embedding = generate_embeddings([query], embedding_model_string)[0]

    mongo_uri = (
        "mongodb+srv://timg51237:01Y4sSZbZxsNFydW@cluster0.qbsk5ke.mongodb.net/?retryWrites=true&w=majority"
    )
    mongodb_client = pymongo.MongoClient(mongo_uri)
    mongodb_db = mongodb_client["beta"]
    mongodb_resumes = mongodb_db["resumes"]

    # Example query.
    results = mongodb_resumes.aggregate([
    {
        "$vectorSearch": {
            "queryVector": vector_embedding,
            "path": vector_database_field_name,
            "numCandidates": 100, # this should be 10-20x the limit
            "limit": 2, # the number of documents to return in the results
            "index": "vector_index", # the index name you used in Step 4.
        }
    }
    ])
    print(results)
    results_as_dict = {doc["text"] for doc in results}
    print(results_as_dict)
    return { "response": results_as_dict }
    

@router.post("/resume_add")
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
    mongodb_resumes.insert_one({ vector_database_field_name: vector_embedding[0], "text": text})

    return { "response": "response"}
    