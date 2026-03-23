# Test2_alexnet - 废弃物分类

本项目使用 AlexNet 网络进行废弃物分类，支持6种类别：纸板(cardboard)、玻璃(glass)、金属(metal)、纸张(paper)、塑料(plastic)和垃圾(trash)。

## 快速开始

### 1. 分割数据集（首次运行）

```bash
python split_data.py
```

将从 `data/dataset-resized/` 分割出 `train/` 和 `val/` 数据集。

### 2. 训练模型

```bash
python train.py
```

模型训练并保存为 `AlexNet.pth`

### 3. 单图像预测

```bash
# 预测指定图像
python predict.py /path/to/your/image.jpg

# 或使用默认图像
python predict.py
```

### 4. 批量预测

Test2_alexnet 暂不包含 batch_predict.py，如需此功能，请参考 Test5_resnet 中的实现。

### 5. 模型评估

```bash
python evaluate.py
```

在验证集上评估模型准确率。

## 文件说明

| 文件 | 功能 |
|------|------|
| `train.py` | 模型训练 |
| `predict.py` | 单图像预测 |
| `evaluate.py` | 模型评估 |
| `split_data.py` | **新增** - 数据分割 |
| `model.py` | AlexNet 模型定义 |
| `class_indices.json` | 类别索引 |

## 主要改动

✅ train.py
- 数据路径改为 `data/dataset-resized`
- 类别数改为 6

✅ predict.py
- 支持命令行传入图像路径
- 默认使用 `data/dataset-resized/cardboard` 中的第一张图像
- 改进输出显示（添加置信度百分比和详细概率分布）

✅ evaluate.py（新增）
- 在验证集上评估模型准确率

✅ split_data.py（新增）
- 从 `data/dataset-resized/` 分割出 train 和 val 数据集

## 6个分类类别
```
0: cardboard(纸板)    3: paper(纸张)
1: glass(玻璃)        4: plastic(塑料)
2: metal(金属)        5: trash(垃圾)
```
