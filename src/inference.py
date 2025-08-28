"""
1. validate schema
2. load model 
3. scoring 
"""

import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import pickle
import random
import uvicorn


# --------------- Schema validations ---------------
class InferenceRequest(BaseModel): 
    age: Annotated[int, Field(ge=0, le=120)]
    gender_code: Literal[0, 1, 2]
    location: Annotated[int, Field(ge=0)]
    subscription_type_code: Literal[0, 1, 2]
    tenure_months: Annotated[int, Field(ge=0)]
    income_bracket_code: Literal[0, 1, 2]
    event_created_at_ts: float
    transaction_value: Annotated[float, Field(ge=0)]
    channel_code: Literal[0, 1]

class InferenceResponse(BaseModel): 
    fraud_flag: bool 
    fraud_probability: float = Annotated[float, Field(ge=0.0, le=1.0)]


# --------------- Model wrapper ---------------
class FraudModel: 
    def __init__(self, model_path: str) -> None:
        self.model = None 
        if model_path and os.path.exists(model_path): 
            try: 
                with open(model_path, 'rb') as f: 
                    self.model = pickle.load(f)
            except Exception as e:
                print("Failed to load XGBoost model") # better log this

    def predict_proba(self, features: InferenceRequest) -> float:
        if self.model is not None: 
            x = pd.DataFrame([features.model_dump()])
            return float(self.model.predict_proba(x)[:, 1][0])
       # return dummy scores 
        return random.random()

def build_model() -> FraudModel: 
    model_path = os.environ.get("FRAUD_MODEL_PATH", "fraud_model.pkl")
    return FraudModel(model_path)


# --------------- FastAPI setup ---------------
app = FastAPI()
model = build_model() 

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post('/infer', response_model=InferenceResponse)
def infer(request: InferenceRequest) -> InferenceResponse:
    try: 
        score = model.predict_proba(request)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Error while scoring: {e}")
    return InferenceResponse(fraud_flag=bool(score>=0.5), fraud_probability=score)


if __name__ == "__main__": 
    uvicorn.run("inference:app",)