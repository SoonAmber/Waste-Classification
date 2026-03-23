import os
import sys

import torch
from torchvision import transforms, datasets
from tqdm import tqdm

from model import resnet34


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    data_root = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # get data root path
    image_path = os.path.join(data_root, "data")  # waste classification data set path
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)

    validate_dataset = datasets.ImageFolder(root=os.path.join(image_path, "val"),
                                            transform=data_transform)
    val_num = len(validate_dataset)

    batch_size = 16
    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])  # number of workers
    print('Using {} dataloader workers every process'.format(nw))

    validate_loader = torch.utils.data.DataLoader(validate_dataset,
                                                  batch_size=batch_size, shuffle=False,
                                                  num_workers=nw)

    print("using {} images for validation.".format(val_num))
    
    # create model
    model = resnet34(num_classes=6)

    # load model weights
    weights_path = "./resNet34.pth"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()

    # evaluate on validation set
    acc = 0.0  # accumulate accurate number
    loss_sum = 0.0
    sample_num = 0
    
    print("\n" + "=" * 60)
    print("Evaluating on Validation Set")
    print("=" * 60)
    
    with torch.no_grad():
        val_bar = tqdm(validate_loader, file=sys.stdout)
        for val_data in val_bar:
            val_images, val_labels = val_data
            outputs = model(val_images.to(device))
            predict_y = torch.max(outputs, dim=1)[1]
            acc += torch.eq(predict_y, val_labels.to(device)).sum().item()
            sample_num += val_labels.size(0)

            val_bar.desc = "Evaluating Progress"

    val_accurate = acc / val_num

    print("\n" + "=" * 60)
    print("Evaluation Results")
    print("=" * 60)
    print("Validation Accuracy: {:.4f} ({}/{})".format(val_accurate, int(acc), val_num))
    print("Correct Predictions: {}".format(int(acc)))
    print("Total Samples: {}".format(val_num))
    print("Error Rate: {:.4f}".format(1.0 - val_accurate))
    print("=" * 60)


if __name__ == '__main__':
    main()
