# import os
# import azure.functions as func
# import numpy as np
# import logging
# import json

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# SIM_INDICES = None
# SIM_SCORES = None

# def load_similarities_once():
#     global SIM_INDICES, SIM_SCORES

#     if SIM_INDICES is not None:
#         return

#     filepath = "models/top20_cosine_sim.pkl"
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"File not found: {filepath}")
    
#     logging.info("Retrieving similarities from storage")
#     data = np.load(filepath, allow_pickle=True)
#     logging.info("Similarities retrieved from storage")
#     logging.info("Building matrices")
#     SIM_INDICES = data["indices"]
#     SIM_SCORES = data["scores"]
#     logging.info("Similarities loaded into memory")



# @app.route(route="recommandation")
# def recommandation(req: func.HttpRequest) -> func.HttpResponse:
#     # load_similarities_once()

#     article_id = req.params.get('article_id')
#     if not article_id:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             return func.HttpResponse("Missing article_id", status_code=400)
#         else:
#             article_id = req_body.get('article_id')

#     article_id = int(article_id)

#     if article_id:
#         return func.HttpResponse(f"Hello, {article_id}. This HTTP triggered function executed successfully.")
    
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
    # recommendations = SIM_INDICES[article_id][:5].tolist()
    # return func.HttpResponse(
    #     json.dumps({
    #         "article_id": article_id,
    #         "recommendations": recommendations
    #     }),
    #     mimetype="application/json"
    # )


import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="recommandation")
def recommandation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
