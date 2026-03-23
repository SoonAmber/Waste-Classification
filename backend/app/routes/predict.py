from fastapi import APIRouter, UploadFile, File, Form
import os
import shutil
from app.services.model_service import model_loader
from app.schemas.schemas import PredictionResponse

router = APIRouter(prefix="/api/predict", tags=["predict"])

UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "../../uploads")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/get-models")
def get_available_models():
    return {
        "models": [
            {"id": "alexnet", "name": "AlexNet", "description": "Fast CNN model"},
            {"id": "resnet", "name": "ResNet-34", "description": "Balanced performance"},
            {"id": "densenet", "name": "DenseNet-121", "description": "High accuracy"},
            {"id": "vit", "name": "Vision Transformer", "description": "State-of-the-art"}
        ]
    }

@router.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...), model_name: str = Form(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    class_name, confidence, all_predictions = model_loader.predict(file_path, model_name)
    os.remove(file_path)
    
    return PredictionResponse(
        class_name=class_name,
        confidence=confidence,
        all_predictions=all_predictions
    )

@router.get("/health")
def health_check():
    return {"status": "ok"}
