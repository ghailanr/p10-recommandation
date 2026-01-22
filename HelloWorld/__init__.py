import os
import logging
import pickle
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import json

SIM_INDICES = None
SIM_SCORES = None

def load_similarities_once():
    global SIM_INDICES, SIM_SCORES

    if SIM_INDICES is not None:
        return

    logging.info("Cold start: loading similarities from Blob Storage...")

    # connect_str = os.environ["ocp10_STORAGE"]
    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # blob_client = blob_service_client.get_blob_client(
    #     container="embeddings",
    #     blob="top20_cosine_sim.pkl"
    # )

    # blob_data = blob_client.download_blob().readall()

    # data = pickle.loads(blob_data)

    data = pickle.load(open("models/top20_cosine_sim.pkl", "rb"))

    SIM_INDICES = data["indices"]
    SIM_SCORES = data["scores"]

    logging.info("Similarities loaded into memory")

def main(req: func.HttpRequest) -> func.HttpResponse:
    load_similarities_once()

    article_id = req.params.get("article_id")
    if article_id is None:
        return func.HttpResponse("Missing article_id", status_code=400)

    article_id = int(article_id)

    recommendations = SIM_INDICES[article_id][:5].tolist()

    return func.HttpResponse(
        json.dumps({
            "article_id": article_id,
            "recommendations": recommendations
        }),
        mimetype="application/json"
    )
