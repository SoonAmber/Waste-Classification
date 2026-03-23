import torch
from torchvision import transforms
from PIL import Image
import os
from typing import Dict, Tuple
import importlib.util

PYTORCH_CLASSIFICATION_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../pytorch_classification")
)

def load_module_from_file(file_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ModelLoader:
    GARBAGE_CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
    
    MODELS = {
        'alexnet': {'dir': 'Test2_alexnet', 'builder': 'AlexNet', 'weights': 'AlexNet.pth'},
        'resnet': {'dir': 'Test5_resnet', 'builder': 'resnet34', 'weights': 'resNet34.pth'},
        'densenet': {'dir': 'Test8_densenet', 'builder': 'densenet121', 'weights': 'weights/model-6.pth'},
        'vit': {'dir': 'vision_transformer', 'builder': 'vit_base_patch16_224', 'weights': None}
    }
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def predict(self, image_path: str, model_name: str) -> Tuple[str, float, Dict[str, float]]:
        model_config = self.MODELS[model_name]
        model_dir = os.path.join(PYTORCH_CLASSIFICATION_PATH, model_config['dir'])
        
        model_file =os.path.join(model_dir, "model.py" if model_name != 'vit' else "vit_model.py")
        module = load_module_from_file(model_file, f"{model_name}_module")
        
        ModelClass = getattr(module, model_config['builder'])
        model = ModelClass(num_classes=6)
        
        weights_path = os.path.join(model_dir, model_config['weights']) if model_config['weights'] else None
        if weights_path and os.path.exists(weights_path):
            model.load_state_dict(torch.load(weights_path, map_location=self.device))
        
        model.to(self.device)
        model.eval()
        
        data_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        img = Image.open(image_path).convert('RGB')
        img_tensor = data_transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = self.GARBAGE_CLASSES[predicted_idx.item()]
        all_predictions = {
            self.GARBAGE_CLASSES[i]: float(prob.item())
            for i, prob in enumerate(probabilities[0])
        }
        all_predictions = dict(sorted(all_predictions.items(), key=lambda x: x[1], reverse=True))
        
        return predicted_class, float(confidence.item()), all_predictions

model_loader = ModelLoader()
