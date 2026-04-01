from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from predict import predict_fruit

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    try:
        file_location = f"temp_{file.filename}"

        # Save uploaded image
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run prediction
        fruit, confidence = predict_fruit(file_location)

        # Delete temp file
        os.remove(file_location)

        return {
            "fruit": fruit,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}
    

@app.get("/model-info")
def model_info():
    return {
        "model": "Fruit Classification CNN",
        "accuracy": 0.94,
        "classes": [
            "Apple",
            "Banana",
            "Orange",
            "Mango",
            "Strawberry"
        ]
    }