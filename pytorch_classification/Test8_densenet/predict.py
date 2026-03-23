import os
import json

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from model import densenet121


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image - 支持输入图像路径
    img_path = "test_image.jpg"  # 默认测试图像路径
    if not os.path.exists(img_path):
        print(f"Warning: {img_path} does not exist. Using first image from dataset for testing.")
        # 如果没有测试图像，使用数据集中的第一个图像
        dataset_path = "../../data/dataset-resized"
        if os.path.exists(dataset_path):
            classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
            if classes:
                first_class_path = os.path.join(dataset_path, classes[0])
                images = [f for f in os.listdir(first_class_path) if f.endswith(('.jpg', '.JPG', '.png', '.PNG'))]
                if images:
                    img_path = os.path.join(first_class_path, images[0])
    
    if not os.path.exists(img_path):
        print("Error: No image found for testing!")
        return
    
    img = Image.open(img_path)
    plt.imshow(img)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = densenet121(num_classes=6).to(device)
    # load model weights
    model_weight_path = "./weights/model-9.pth"
    if os.path.exists(model_weight_path):
        model.load_state_dict(torch.load(model_weight_path, map_location=device))
    else:
        print(f"Warning: Model weights {model_weight_path} not found. Using pretrained weights.")
    
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()
        
        # 获取预测的准确率（置信度）
        confidence = predict[predict_cla].numpy()

    print_res = "class: {}   confidence: {:.4f}".format(class_indict[str(predict_cla)],
                                                        confidence)
    plt.title(print_res)
    for i in range(len(predict)):
        print("class: {:10}   probability: {:.4f}".format(class_indict[str(i)],
                                                          predict[i].numpy()))
    plt.show()


if __name__ == '__main__':
    main()
