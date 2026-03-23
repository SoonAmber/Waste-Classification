import os
import json
import sys

import torch
from PIL import Image
from torchvision import transforms

from model import resnet34


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image
    # 指向需要遍历预测的图像文件夹
    if len(sys.argv) > 1:
        imgs_root = sys.argv[1]
    else:
        # default to the waste classification data validation set
        imgs_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/dataset-resized/cardboard"))
    
    assert os.path.exists(imgs_root), f"file: '{imgs_root}' does not exist."
    
    # 读取指定文件夹下所有图像路径(支持多种格式)
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    img_path_list = [os.path.join(imgs_root, i) for i in os.listdir(imgs_root) 
                     if any(i.lower().endswith(ext) for ext in img_extensions)]
    
    if not img_path_list:
        print(f"No images found in {imgs_root}")
        return

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), f"file: '{json_path}' does not exist."

    with open(json_path, "r") as json_file:
        class_indict = json.load(json_file)

    # create model
    model = resnet34(num_classes=6).to(device)

    # load model weights
    weights_path = "./resNet34.pth"
    if not os.path.exists(weights_path):
        print(f"Warning: model weights file '{weights_path}' not found.")
        print("Please train the model first using train.py")
        return
    
    model.load_state_dict(torch.load(weights_path, map_location=device))

    # prediction
    model.eval()
    batch_size = 8  # 每次预测时将多少张图片打包成一个batch
    with torch.no_grad():
        for ids in range(0, (len(img_path_list) + batch_size - 1) // batch_size):
            img_list = []
            batch_img_paths = []
            for img_path in img_path_list[ids * batch_size: (ids + 1) * batch_size]:
                assert os.path.exists(img_path), f"file: '{img_path}' does not exist."
                try:
                    img = Image.open(img_path)
                    # Convert RGBA to RGB if necessary
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img = data_transform(img)
                    img_list.append(img)
                    batch_img_paths.append(img_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
                    continue

            if not img_list:
                continue
                
            # batch img
            # 将img_list列表中的所有图像打包成一个batch
            batch_img = torch.stack(img_list, dim=0)
            # predict class
            output = model(batch_img.to(device)).cpu()
            predict = torch.softmax(output, dim=1)
            probs, classes = torch.max(predict, dim=1)

            for idx, (pro, cla) in enumerate(zip(probs, classes)):
                print("image: {:50}  class: {:12}  prob: {:.4f}".format(
                    os.path.basename(batch_img_paths[idx]),
                    class_indict[str(cla.numpy())],
                    pro.numpy()))


if __name__ == '__main__':
    main()
