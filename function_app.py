import azure.functions as func
import logging
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="recommandation")
def recommandation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('*Loading files for recommandation function*')

    filepath = "models/top20_cosine_sim.pkl"
    with open(filepath, 'rb') as f:
        top20_cosine_sim = pd.read_pickle(f)

    logging.info('Files loaded successfully.')

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
