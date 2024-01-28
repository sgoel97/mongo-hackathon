from enum import Enum

class VectorStoreProvider(str, Enum):
    WEAVIATE = "weaviate"
    CUSTODIED = "custodied"
    AWS = "aws"
    SELF_HOSTED = "self_hosted"
