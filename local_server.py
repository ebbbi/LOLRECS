import uvicorn
import os
from app.champ_classification.models import CNNmodel

if __name__ == "__main__":
    os.environ["RIOT_API_KEY"] = "RGAPI-9f4aec3a-1cf1-4b6c-8079-37bab48ac7b7"
    os.environ['DB_NAME'] = "DB_NAME"
    os.environ['DB_API_ENDPOINT'] = "DB_API_ENDPOINT"
    uvicorn.run("app.main:app", host="localhost", port=8080, reload=True)
