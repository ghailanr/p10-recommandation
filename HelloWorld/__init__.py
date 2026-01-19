import logging
import json
import azure.functions as func
import pickle
#import numpy as np
import faiss
import time
import os
from azure.storage.blob import BlobServiceClient

EMBEDDINGS = None
NEIGHBORS = None
INITIALIZED = False
TOP_K = 20

def load_embeddings():
    global EMBEDDINGS
    if EMBEDDINGS is not None:
        return

    logging.info("Loading embeddings from Blob Storage...")
    #conn = os.environ["ocp10_STORAGE"] //Local Execution only
    conn = os.getenv("AzureWebJobsStorage")
    blob_service = BlobServiceClient.from_connection_string(conn)
    blob = blob_service.get_blob_client(
        container="embeddings",
        blob="embeddings_pca.pkl"
    )

    EMBEDDINGS = pickle.loads(blob.download_blob().readall())
    logging.info("Embeddings loaded.")

def initialize_index():
    global INITIALIZED, NEIGHBORS

    logging.info("Cold start: initializing recommender...")

    # Normalize
    faiss.normalize_L2(EMBEDDINGS)

    d = EMBEDDINGS.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(EMBEDDINGS)

    # Compute neighbors
    _, I = index.search(EMBEDDINGS, TOP_K + 1)

    # Remove self
    NEIGHBORS = {
        i: I[i][1:].tolist()
        for i in range(len(I))
    }

    INITIALIZED = True
    logging.info("Initialization complete")

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()
    global INITIALIZED

    if not INITIALIZED:
        load_embeddings()
        initialize_index()
        logging.info(f"Initialization time: {time.time() - start_time:.2f} seconds")

    article_id = int(req.params.get("article_id", -1))

    if article_id < 0 or article_id not in NEIGHBORS:
        return func.HttpResponse("Invalid article_id", status_code=400)

    formulating_answer_start = time.time()
    response = func.HttpResponse(
        json.dumps({
            "article_id": article_id,
            "recommendations": NEIGHBORS[article_id][:5]
        }),
        mimetype="application/json"
    )
    logging.info(f"Answer formulation time: {time.time() - formulating_answer_start:.2f} seconds")
    return response

