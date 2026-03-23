# 废弃物分类 ResNet34 模型

本项目使用 ResNet34 网络进行废弃物分类，支持6种类别：纸板(cardboard)、玻璃(glass)、金属(metal)、纸张(paper)、塑料(plastic)和垃圾(trash)。

## 项目结构

```
Test5_resnet/
├── model.py                          # ResNet34 模型定义
├── train.py                          # 训练脚本
├── predict.py                        # 单图像预测脚本
├── batch_predict.py                  # 批量预测脚本
├── load_weights.py                   # 权重加载脚本
├── split_data.py                     # 数据集分割脚本
├── class_indices.json                # 类别索引（自动生成）
└── resNet34.pth                      # 训练后的模型权重
```

## 前置要求

### 必需的依赖包

```bash
pip install torch torchvision pillow matplotlib tqdm
```

### 预训练模型

需要下载预训练的 ResNet34 模型权重，命名为 `resnet34-pre.pth`

下载地址：https://download.pytorch.org/models/resnet34-333f7ec4.pth

将下载的文件放在 `Test5_resnet` 目录下，并重命名为 `resnet34-pre.pth`

## 数据准备

### 1. 数据分割

如果你的数据还没有分割成 train/val 集，使用以下脚本：

```bash
python split_data.py
```

**说明：**
- 此脚本会从 `data/dataset-resized/` 中读取原始数据
- 将数据随机分割为 90% 训练集和 10% 验证集
- 在 `data/` 目录下创建 `train/` 和 `val/` 文件夹

### 2. 数据格式

数据应按照以下结构组织：

```
data/
├── dataset-resized/
│   ├── cardboard/
│   │   ├── img1.jpg
│   │   └── ...
│   ├── glass/
│   │   └── ...
│   ├── metal/
│   │   └── ...
│   ├── paper/
│   │   └── ...
│   ├── plastic/
│   │   └── ...
│   └── trash/
│       └── ...
```

分割后会生成：

```
data/
├── train/
│   ├── cardboard/
│   ├── glass/
│   ├── metal/
│   ├── paper/
│   ├── plastic/
│   └── trash/
└── val/
    ├── cardboard/
    ├── glass/
    ├── metal/
    ├── paper/
    ├── plastic/
    └── trash/
```

## 模型训练

### 基本训练

```bash
python train.py
```

**训练参数（可在 train.py 中修改）：**
- `batch_size`: 16 (批大小)
- `epochs`: 3 (训练轮数)
- `learning_rate`: 0.0001 (学习率)
- 优化器: Adam

### 训练过程

1. 加载预训练的 ResNet34 权重
2. 修改最后的全连接层为 6 个输出节点（对应6个类别）
3. 使用训练集训练模型
4. 在验证集上评估模型性能
5. 保存最佳模型权重到 `resNet34.pth`

### 输出示例

```
using cuda:0 device.
Using 8 dataloader workers every process
using xxxx images for training, xxx images for validation.
train epoch[1/3] loss:1.234: 100%|████████| 100/100 [02:15<00:00,  1.35s/it]
valid epoch[1/3]: 100%|████████| 25/25 [00:15<00:00,  1.60it/s]
...
```

## 模型预测

### 1. 单图像预测

**方法1：指定图像路径**

```bash
python predict.py /path/to/image.jpg
```

**方法2：使用默认图像**

```bash
python predict.py
```

将使用 `data/dataset-resized/cardboard/` 中的第一张图像进行预测。

### 预测输出

预测结果包含：
- 原始图像显示
- 预测结果的柱状图（显示各类别的概率）
- 详细的类别概率输出

```
==================================================
Prediction Results:
==================================================
Image: image.jpg
Predicted class: cardboard
Confidence: 0.9523

All class probabilities:
class: cardboard      prob: 0.9523
class: glass         prob: 0.0312
class: metal         prob: 0.0089
class: paper         prob: 0.0054
class: plastic       prob: 0.0019
class: trash         prob: 0.0003
```

### 2. 批量预测

**预测指定文件夹中的所有图像：**

```bash
python batch_predict.py /path/to/image/folder
```

**使用默认文件夹：**

```bash
python batch_predict.py
```

将使用 `data/dataset-resized/cardboard/` 中的所有图像进行预测。

### 批量预测输出

```
image: img1.jpg                          class: cardboard     prob: 0.9523
image: img2.jpg                          class: glass         prob: 0.8741
image: img3.jpg                          class: metal         prob: 0.7623
...
```

## 高级用法

### 修改训练参数

在 `train.py` 中修改以下参数：

```python
batch_size = 32          # 增加批大小
epochs = 10              # 增加训练轮数
optimizer = optim.SGD(params, lr=0.001)  # 改用SGD优化器
```

### 使用 GPU

自动根据设备选择 CUDA（如果可用）。若强制使用 CPU：

```python
device = torch.device("cpu")
```

### 加载预训练权重

使用 `load_weights.py` 脚本加载预训练权重：

```bash
python load_weights.py
```

## 常见问题

### Q: 模型权重文件 resnet34-pre.pth 在哪里？
**A:** 需要从 PyTorch 官方下载：https://download.pytorch.org/models/resnet34-333f7ec4.pth

### Q: 运行 predict.py 时报错 "model weights file not found"？
**A:** 需要先运行 train.py 来训练模型并生成 resnet34-pre.pth 文件。

### Q: 数据分割后应该删除原始数据吗？
**A:** 不需要删除，原始数据可以保留，train/val 文件夹是复制而不是移动。

### Q: 如何在一个已训练的模型上继续训练？
**A:** 在 train.py 中加载已有的模型权重而不是预训练权重：
```python
model_weight_path = "./resNet34.pth"
```

## 类别说明

| 类别号 | 类别名称 | 说明 |
|--------|---------|------|
| 0 | cardboard | 纸板 |
| 1 | glass | 玻璃 |
| 2 | metal | 金属 |
| 3 | paper | 纸张 |
| 4 | plastic | 塑料 |
| 5 | trash | 垃圾 |

## 参考资源

- ResNet 论文: https://arxiv.org/abs/1512.03385
- PyTorch 官方文档: https://pytorch.org/docs/
- ImageNet 预训练模型: https://pytorch.org/vision/stable/models.html

## 许可证

本项目遵循原始仓库的许可证。

## 更新日志

- 2024年: 修改为支持废弃物分类数据集（6个类别）
- 添加了数据分割脚本
- 改进了预测脚本的可用性和输出格式
- 添加了批量预测功能
