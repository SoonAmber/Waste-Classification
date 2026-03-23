from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """创建用户的请求模型"""
    password: str

class UserLogin(BaseModel):
    """登录请求模型"""
    username: str
    password: str

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str
    user: UserResponse

class PredictionRequest(BaseModel):
    """预测请求模型"""
    model_name: str  # 模型名称: 'alexnet', 'resnet', 'densenet', 'vit'

    model_config = ConfigDict(protected_namespaces=())

class PredictionResponse(BaseModel):
    """预测响应模型"""
    class_name: str
    confidence: float
    all_predictions: dict
    
    model_config = ConfigDict(protected_namespaces=())
