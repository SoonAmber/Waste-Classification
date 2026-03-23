import os
import json
import torch
from torchvision import transforms
from tqdm import tqdm

from model import densenet121, load_state_dict
from my_dataset import MyDataSet
from utils import read_split_data


def evaluate_model(model, data_loader, device, num_classes):
    """评估模型在数据集上的性能"""
    model.eval()
    acc = 0.0
    class_correct = [0] * num_classes
    class_total = [0] * num_classes
    
    with torch.no_grad():
        for data in tqdm(data_loader, desc="Evaluating"):
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            # 获取预测类别
            _, predicted = torch.max(outputs.data, 1)
            
            # 计算总准确率
            acc += (predicted == labels).sum().item()
            
            # 计算每个类别的准确率
            correct = (predicted == labels).squeeze()
            for i in range(len(labels)):
                label = labels[i]
                class_correct[label] += correct[i].item() if correct.dim() > 0 else (1 if correct.item() else 0)
                class_total[label] += 1
    
    acc = acc / len(data_loader.dataset)
    
    return acc, class_correct, class_total


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 数据集路径
    data_path = "../../data/dataset-resized"
    
    # 数据变换
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 读取class_indices
    json_path = './class_indices.json'
    with open(json_path, "r") as f:
        class_indices = json.load(f)
    
    num_classes = len(class_indices)
    
    # 读取数据集
    train_images_path, train_images_label, val_images_path, val_images_label = read_split_data(data_path)
    
    # 创建验证数据集
    val_dataset = MyDataSet(images_path=val_images_path,
                            images_class=val_images_label,
                            transform=data_transform)
    
    # 创建验证数据加载器
    batch_size = 12
    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])
    val_loader = torch.utils.data.DataLoader(val_dataset,
                                             batch_size=batch_size,
                                             shuffle=False,
                                             pin_memory=True,
                                             num_workers=nw,
                                             collate_fn=val_dataset.collate_fn)
    
    # 加载模型
    model = densenet121(num_classes=num_classes).to(device)
    
    # 加载权重
    model_weight_path = "./weights/model-9.pth"
    if os.path.exists(model_weight_path):
        model.load_state_dict(torch.load(model_weight_path, map_location=device))
        print(f"Loaded weights from {model_weight_path}")
    else:
        print(f"Warning: Model weights {model_weight_path} not found!")
        # 寻找最新的权重文件
        weights_dir = "./weights"
        if os.path.exists(weights_dir):
            weight_files = [f for f in os.listdir(weights_dir) if f.endswith('.pth')]
            if weight_files:
                latest_weight = max(weight_files, key=lambda x: int(x.split('-')[1].split('.')[0]))
                model_weight_path = os.path.join(weights_dir, latest_weight)
                model.load_state_dict(torch.load(model_weight_path, map_location=device))
                print(f"Loaded weights from {model_weight_path}")
    
    # 评估模型
    print("\nEvaluating on validation set...")
    val_acc, class_correct, class_total = evaluate_model(model, val_loader, device, num_classes)
    
    print(f"\nValidation Accuracy: {val_acc:.4f}")
    print("\nPer-class Accuracy:")
    for i in range(num_classes):
        if class_total[i] > 0:
            class_acc = class_correct[i] / class_total[i]
            print(f"  {class_indices[str(i)]:12} : {class_acc:.4f} ({class_correct[i]}/{class_total[i]})")
        else:
            print(f"  {class_indices[str(i)]:12} : No samples")


if __name__ == '__main__':
    main()
