from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.predict import predict_digit

app = FastAPI()

class PredictRequest(BaseModel):
    image_base64: str

class PredictResponse(BaseModel):
    prediction: int

@app.post("/predict", response_model=PredictResponse, summary="Handwritten Digit Prediction", tags=["MNIST"])
def predict(req: PredictRequest):
    try:
        result = predict_digit(req.image_base64)
        return {"prediction": result}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Input error：{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Reference fail, try later")