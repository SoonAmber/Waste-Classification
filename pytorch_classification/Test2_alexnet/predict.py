import os
import json
import sys

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from model import AlexNet


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize((224, 224)),
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    # load image
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        # default image path
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/dataset-resized/cardboard"))
        # find first image in the directory
        img_list = [f for f in os.listdir(img_path) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp'))]
        if img_list:
            img_path = os.path.join(img_path, img_list[0])
        else:
            print("No images found in default path. Please provide an image path as argument.")
            return
    
    assert os.path.exists(img_path), "file: '{}' does not exist.".format(img_path)
    img = Image.open(img_path)
    
    # display original image
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original Image")
    plt.axis('off')
    
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' does not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = AlexNet(num_classes=6).to(device)

    # load model weights
    weights_path = "./AlexNet.pth"
    if not os.path.exists(weights_path):
        print(f"Warning: model weights file '{weights_path}' not found.")
        print("Please train the model first using train.py")
        return
    model.load_state_dict(torch.load(weights_path, map_location=device))

    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    # display prediction result
    plt.subplot(1, 2, 2)
    class_names = list(class_indict.values())
    probabilities = [predict[i].numpy() for i in range(len(predict))]
    
    colors = ['#ff7f0e' if i == predict_cla else '#1f77b4' for i in range(len(class_names))]
    plt.barh(class_names, probabilities, color=colors)
    plt.xlabel('Probability')
    plt.title('Prediction Results')
    plt.xlim([0, 1])
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "=" * 60)
    print("Prediction Results")
    print("=" * 60)
    print(f"Image: {os.path.basename(img_path)}")
    print(f"Predicted class: {class_indict[str(predict_cla)]}")
    print(f"Confidence: {predict[predict_cla].numpy():.4f} ({predict[predict_cla].numpy()*100:.2f}%)")
    print("\nDetailed Probabilities for All Classes:")
    print("-" * 60)
    for i in range(len(predict)):
        prob = predict[i].numpy()
        print("class: {:12}   prob: {:.4f}  ({:6.2f}%)".format(
            class_indict[str(i)],
            prob,
            prob * 100))
    print("=" * 60)


if __name__ == '__main__':
    main()
