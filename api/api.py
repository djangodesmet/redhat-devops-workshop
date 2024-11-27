import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from gliner import GLiNER
from huggingface_hub.errors import HFValidationError
from pydantic import BaseModel


# load model on startup of API
@asynccontextmanager
async def lifespan(app: FastAPI):  # TODO: download model from s3 to local
    model_path = "./models"
    try:
        model = GLiNER.from_pretrained(
            "./models",
            load_onnx_model=True,
            onnx_model_file="onnx/model.onnx",
            load_tokenizer=True,
            local_files_only=True,
        )
    except HFValidationError as e:
        logging.error(
            f"Model not found in {model_path}. Make sure the model is downloaded."
        )
        raise e
    # put model in "state" so it can be retrieved later via request.state
    yield {"model": model}


app = FastAPI(lifespan=lifespan)


class PredictionsBody(BaseModel):
    text: str
    labels: list[str]
    threshold: float


class PredictionResult(BaseModel):
    entities: list[dict]


@app.post("/predict")
async def predict(data: PredictionsBody, request: Request) -> PredictionResult:
    """Endpoint for generating predictions based on input data.

    Args:
        data (PredictionsBody): Incoming object to make predictions for.

    Returns:
        PredictionResult: A PredictionResult containing entities.
    """
    entities = request.state.model.predict_entities(
        data.text, data.labels, threshold=data.threshold, multi_label=True
    )
    return PredictionResult(entities=entities)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    logging.info("Launching API..")
    uvicorn.run(app, host="0.0.0.0", port=9000)
