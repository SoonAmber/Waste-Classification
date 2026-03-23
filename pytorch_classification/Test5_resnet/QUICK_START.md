# 快速开始指南

## 5分钟快速上手

### 第1步：下载预训练模型（一次性）

```bash
# 进入Test5_resnet目录
cd pytorch_classification/Test5_resnet

# 下载resnet34预训练权重
# Windows用户可以使用浏览器访问以下链接下载，然后放在该目录下，重命名为resnet34-pre.pth
# https://download.pytorch.org/models/resnet34-333f7ec4.pth

# 或者使用Python下载
python -c "
import urllib.request
url = 'https://download.pytorch.org/models/resnet34-333f7ec4.pth'
urllib.request.urlretrieve(url, 'resnet34-pre.pth')
print('下载完成！')
"
```

### 第2步：分割数据集

```bash
python split_data.py
```

这将从 `data/dataset-resized/` 分割出 `train/` 和 `val/` 数据集。

### 第3步：训练模型

```bash
python train.py
```

等待训练完成（通常需要几分钟到几十分钟，取决于数据量和硬件）。

### 第4步：单图像预测

```bash
# 预测指定图像
python predict.py path/to/your/image.jpg

# 或使用默认图像
python predict.py
```

### 第5步：批量预测

```bash
# 预测文件夹中的所有图像
python batch_predict.py path/to/image/folder

# 或使用默认文件夹
python batch_predict.py
```

## 主要改动说明

该项目已从花卉分类修改为 **废弃物分类**，支持以下6个类别：

| 类别 | 说明 |
|------|------|
| cardboard | 纸板 |
| glass | 玻璃 |
| metal | 金属 |
| paper | 纸张 |
| plastic | 塑料 |
| trash | 垃圾 |

## 文件说明

### 核心脚本

| 文件 | 功能 |
|------|------|
| `train.py` | 模型训练脚本 |
| `predict.py` | 单图像预测脚本（支持传入图像路径或使用默认） |
| `batch_predict.py` | 批量预测脚本 |
| `split_data.py` | **新增** 数据分割脚本 |
| `model.py` | ResNet34模型定义 |
| `load_weights.py` | 权重加载辅助脚本 |

### 配置文件

| 文件 | 功能 |
|------|------|
| `class_indices.json` | 类别索引定义（自动生成/更新） |
| `resnet34-pre.pth` | 预训练的ResNet34权重 |
| `resNet34.pth` | 训练后的模型权重（训练后生成） |

## 关键改动

✅ **train.py**
- 数据路径改为 `data/dataset-resized`（原为 `data_set/flower_data`）
- 输出类别数改为 6（原为 5）

✅ **predict.py**
- 支持命令行传入图像路径
- 默认使用 `data/dataset-resized/cardboard` 中的第一张图像
- 改进了输出显示（添加了预测概率柱状图）

✅ **batch_predict.py**
- 支持命令行传入文件夹路径
- 输出类别数改为 6（原为 5）
- 改进了容错能力（支持多种图像格式，异常图像不中断处理）

✅ **新增 split_data.py**
- 从 `data/dataset-resized/` 随机分割出 train/val 数据集
- 默认分割比例为 90% train，10% val

✅ **class_indices.json**
- 更新为6个新类别（原为5个花卉类别）

## 使用示例

### 示例1：完整的训练-预测流程

```bash
# 1. 进入目录
cd pytorch_classification/Test5_resnet

# 2. 分割数据（首次运行）
python split_data.py

# 3. 训练模型
python train.py

# 4. 预测单个图像
python predict.py ../../data/dataset-resized/cardboard/example.jpg

# 5. 批量预测
python batch_predict.py ../../data/dataset-resized/glass
```

### 示例2：使用已有的模型进行预测

```bash
# 直接预测（无需训练）
python predict.py your_image.jpg
python batch_predict.py your_image_folder
```

## 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `resnet34-pre.pth not found` | 缺少预训练权重 | 下载预训练模型 |
| `data path does not exist` | 数据路径不对 | 检查 `data/dataset-resized` 是否存在 |
| `resNet34.pth not found` | 缺少训练后的权重 | 运行 `train.py` 进行训练 |
| `No images found` | 预测文件夹为空 | 检查文件夹路径和文件格式 |

## 性能预期

在标准GPU（如RTX 2060）上：
- **训练速度**：每个epoch约2-5分钟（取决于数据量）
- **预测速度**：单张图像 <100ms；批量预测8张图像 <200ms
- **精度**：使用预训练权重微调后通常可达 85%+ 准确率

## 更多信息

详见 `README_WASTE_CLASSIFICATION.md` 获得完整的项目文档。
