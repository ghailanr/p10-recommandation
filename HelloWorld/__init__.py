import logging
import azure.functions as func
import os
import pickle
from azure.storage.blob import BlobServiceClient

# -----------------------
# Chargement au cold start
# -----------------------

EMBEDDINGS_CONTAINER = os.getenv("ocp10", "embeddings")
EMBEDDINGS_BLOB_PATH = "embeddings/embeddings_pca.pkl"

embeddings = None

try:
    logging.info("Initializing BlobServiceClient...")
    
    blob_service_client = BlobServiceClient.from_connection_string(
        os.environ["AzureWebJobsStorage"]
    )

    container_client = blob_service_client.get_container_client(
        EMBEDDINGS_CONTAINER
    )

    blob_client = container_client.get_blob_client(EMBEDDINGS_BLOB_PATH)

    logging.info("Downloading embeddings from Blob Storage...")
    blob_data = blob_client.download_blob().readall()

    embeddings = pickle.loads(blob_data)

    logging.info(
        f"Embeddings loaded successfully. "
        f"Type={type(embeddings)}, "
        f"Size={len(embeddings) if hasattr(embeddings, '__len__') else 'N/A'}"
    )

except Exception as e:
    logging.error("Failed to load embeddings at startup", exc_info=e)
    embeddings = None


# -----------------------
# HTTP Trigger
# -----------------------

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello World", status_code=200)

