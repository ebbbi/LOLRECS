import uvicorn
from app.champ_classification.models import CNNmodel

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80)
