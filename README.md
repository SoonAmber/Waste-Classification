# 垃圾分类智能识别系统

全栈 Web 应用，集成深度学习模型进行垃圾图像分类。

## 🚀 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python main.py
# API 文档: http://localhost:8000/docs
```

### 前端启动

```bash
cd Ts
npm install
npm run dev
# 访问: http://localhost:3000
```

## 📁 项目结构

```
├── backend/                      # FastAPI 后端
│   ├── app/
│   │   ├── routes/              # API 路由
│   │   ├── services/            # 业务逻辑
│   │   ├── database/            # 数据库
│   │   └── schemas/             # 数据模型
│   ├── main.py                 # 应用入口
│   └── requirements.txt         # 依赖
│
├── Ts/                          # Next.js 前端
│   ├── src/
│   │   ├── app/                 # 页面
│   │   ├── components/          # 组件
│   │   ├── lib/                 # 工具库
│   │   └── types/               # 类型定义
│   └── package.json
│
└── pytorch_classification/      # 深度学习模型
    ├── Test2_alexnet/
    ├── Test5_resnet/
    ├── Test8_densenet/
    └── vision_transformer/
```

## 🔌 API 文档

### 认证端点

**注册**
```
POST /api/auth/register
{
  "username": "user",
  "email": "user@example.com",
  "password": "password"
}
```

**登录**
```
POST /api/auth/login
{
  "username": "user",
  "password": "password"
}
Response: {
  "access_token": "token",
  "token_type": "bearer",
  "user": {...}
}
```

**获取用户**
```
GET /api/auth/me
Header: Authorization: Bearer {token}
```

### 预测端点

**获取模型**
```
POST /api/predict/get-models
Response: {
  "models": [
    {"id": "alexnet", "name": "AlexNet", "description": "..."},
    {"id": "resnet", "name": "ResNet-34", "description": "..."},
    {"id": "densenet", "name": "DenseNet-121", "description": "..."},
    {"id": "vit", "name": "Vision Transformer", "description": "..."}
  ]
}
```

**预测图像**
```
POST /api/predict/predict
Content-Type: multipart/form-data
file: <image>
model_name: resnet

Response: {
  "class_name": "plastic",
  "confidence": 0.95,
  "all_predictions": {
    "plastic": 0.95,
    "paper": 0.03,
    ...
  }
}
```

## 🛠️ 技术栈

**后端**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PyTorch 2.0.0
- python-jose 3.3.0
- SQLite

**前端**
- Next.js 14.2.35
- React 18.2.0
- TypeScript 5.3.0
- Tailwind CSS 3.3.0
- Zustand 4.4.0
- Axios 1.6.2

## 💻 使用流程

1. **注册账户** - 创建用户名、邮箱和密码
2. **登录** - 获取 JWT 令牌
3. **选择模型** - 从 4 个模型中选择
4. **上传图像** - 支持 jpg, png, gif, webp
5. **查看结果** - 分类标签、置信度、概率分布

## 📊 模型信息

| 模型 | 推理时间 | 大小 | 精度 |
|------|---------|------|------|
| AlexNet | ~50ms | 227MB | ⭐⭐ |
| ResNet-34 | ~80ms | 83MB | ⭐⭐⭐ |
| DenseNet-121 | ~120ms | 32MB | ⭐⭐⭐⭐ |
| Vision Transformer | ~200ms | 330MB | ⭐⭐⭐⭐⭐ |

## 🔧 开发命令

**后端**
```bash
cd backend
python main.py                          # 启动服务
uvicorn main:app --reload              # 热重载
```

**前端**
```bash
cd Ts
npm run dev       # 开发
npm run build     # 构建
npm start         # 生产
```

## 📝 环境变量

**后端 (backend/.env)**
```env
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./users.db
MODEL_DEVICE=cuda
```

**前端 (Ts/.env.local)**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 🎯 核心功能

- ✅ 用户注册/登录（JWT 认证）
- ✅ 4 种深度学习模型
- ✅ 实时图像分类
- ✅ 置信度和概率展示
- ✅ 响应式 UI 设计
- ✅ 拖拽图像上传

## 🐛 常见问题

| 问题 | 解决方案 |
|------|--------|
| CORS 错误 | 检查 main.py 的 allow_origins |
| 模型加载失败 | 确保 pytorch_classification 路径正确 |
| API 连接失败 | 检查 .env.local 中的 API 地址 |
| 推理速度慢 | 使用 GPU 或选择轻量级模型 |

## 📄 许可证

MIT
