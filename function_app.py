import os
import azure.functions as func
import logging
import pickle
import json
import numpy as np

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

SIM_INDICES = None
SIM_SCORES = None

def load_similarities_once():
    global SIM_INDICES, SIM_SCORES

    if SIM_INDICES is not None:
        return

    logging.info("Retrieving similarities from storage")

    # connect_str = os.environ["ocp10_STORAGE"]
    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # blob_client = blob_service_client.get_blob_client(
    #     container="embeddings",
    #     blob="top20_cosine_sim.pkl"
    # )

    # blob_data = blob_client.download_blob().readall()

    # data = pickle.loads(blob_data)

    filepath = "models/top20_cosine_sim.pkl"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    else:
        data = np.load(open(filepath, "rb"), allow_pickle=True)
        # data = pickle.load(open(filepath, "rb"))
        logging.info("Similarities retrieved from storage")
        logging.info("Building matrices")
        SIM_INDICES = data["indices"]
        SIM_SCORES = data["scores"]
        logging.info("Similarities loaded into memory")
    
    

@app.route(route="recommandation")
def recommandation(req: func.HttpRequest) -> func.HttpResponse:
    load_similarities_once()

    article_id = req.params.get('article_id')
    if not article_id:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Missing article_id", status_code=400)
        else:
            article_id = req_body.get('article_id')

    article_id = int(article_id)
    recommendations = SIM_INDICES[article_id][:5].tolist()
    return func.HttpResponse(
        json.dumps({
            "article_id": article_id,
            "recommendations": recommendations
        }),
        mimetype="application/json"
    )