"""
模型加载和预测服务 - 优化版本

将所有模型预测逻辑合并为一个通用的预测接口，
避免了代码重复并提高了可维护性。
"""

import torch
from torchvision import transforms
from PIL import Image
import os
from typing import Dict, Tuple
import json
import importlib.util

PYTORCH_CLASSIFICATION_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../pytorch_classification")
)

def load_module_from_file(file_path: str, module_name: str):
    """从文件路径动态加载模块"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ModelLoader:
    """模型加载器 - 统一接口支持多个深度学习模型"""
    
    GARBAGE_CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
    
    # 模型配置（减少重复，使用配置表驱动）
    MODELS = {
        'alexnet': {
            'dir': 'Test2_alexnet',
            'weights': 'AlexNet.pth',
            'model_file': 'model.py',
            'model_builder': 'AlexNet',
            'transform': transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]),
        },
        'resnet': {
            'dir': 'Test5_resnet',
            'weights': 'resNet34.pth',
            'model_file': 'model.py',
            'model_builder': 'resnet34',
            'transform': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        },
        'densenet': {
            'dir': 'Test8_densenet',
            'weights': 'weights/model-6.pth',
            'model_file': 'model.py',
            'model_builder': 'densenet121',
            'transform': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        },
        'vit': {
            'dir': 'vision_transformer',
            'weights': None,
            'model_file': 'vit_model.py',
            'model_builder': 'vit_base_patch16_224',
            'transform': transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        }
    }
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def _load_class_indices(self, model_dir: str) -> Dict[str, str]:
        """加载类别索引文件"""
        json_path = os.path.join(model_dir, "class_indices.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {str(i): name for i, name in enumerate(self.GARBAGE_CLASSES)}
    
    def predict(self, image_path: str, model_name: str) -> Tuple[str, float, Dict[str, float]]:
        """
        统一预测接口 - 支持所有配置的模型
        
        Args:
            image_path: 图像文件路径
            model_name: 模型名称 ('alexnet', 'resnet', 'densenet', 'vit')
            
        Returns:
            (预测类别, 置信度, 所有类别的概率字典)
        """
        if model_name not in self.MODELS:
            raise ValueError(f"不支持的模型: {model_name}")
        
        config = self.MODELS[model_name]
        model_dir = os.path.join(PYTORCH_CLASSIFICATION_PATH, config['dir'])
        
        if not os.path.exists(model_dir):
            raise RuntimeError(f"模型目录不存在: {model_dir}")
        
        try:
            # 1. 加载模型
            model = self._load_model(model_dir, config)
            
            # 2. 加载和转换图像
            img = Image.open(image_path).convert('RGB')
            img_tensor = config['transform'](img).unsqueeze(0).to(self.device)
            
            # 3. 执行推理
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            # 4. 获取结果
            class_indices = self._load_class_indices(model_dir)
            predicted_class = class_indices.get(
                str(predicted_idx.item()), 
                f"Class {predicted_idx.item()}"
            )
            
            # 5. 构建完整的预测概率（按概率排序）
            all_predictions = {
                class_indices.get(str(idx), f"Class {idx}"): float(prob.item())
                for idx, prob in enumerate(probabilities[0])
            }
            all_predictions = dict(
                sorted(all_predictions.items(), key=lambda x: x[1], reverse=True)
            )
            
            return predicted_class, float(confidence.item()), all_predictions
        
        except Exception as e:
            raise RuntimeError(f"预测失败: {str(e)}")
    
    def _load_model(self, model_dir: str, config: dict):
        """加载模型和权重"""
        model_file_path = os.path.join(model_dir, config['model_file'])
        
        # 动态加载模块
        module = load_module_from_file(model_file_path, f"{config['dir']}_module")
        
        # 获取模型构造函数并创建模型实例
        model_builder = getattr(module, config['model_builder'])
        model = model_builder(num_classes=6)
        
        # 加载权重（如果存在）
        if config['weights']:
            weights_path = os.path.join(model_dir, config['weights'])
            if os.path.exists(weights_path):
                model.load_state_dict(torch.load(weights_path, map_location=self.device))
        
        model.to(self.device)
        model.eval()
        return model


# 全局模型加载器实例
model_loader = ModelLoader()
