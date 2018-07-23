import glob
import random
import os
import numpy as np
import torch

from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

class DeepFashionDataset(Dataset):
    def __init__(self, root, transforms_=None):
        """
        Parameters
        ----------
        root: the root of the DeepFashion dataset. This is the folder
          which contains the subdirectories 'Anno', 'Img', etc.
          It is assumed that in 'Img' the directory 'img_converted'
          exists, which gets created by running the script `resize.sh`.
        """
        self.transform = transforms.Compose(transforms_)
        self.root = root
        # Store information about the dataset.
        self.filenames = None
        self.attrs = None
        self.categories = None
        self.num_files = None
        # Read the metadata files.
        self.get_list_attr_img()
        self.get_list_category_img()

    def get_list_attr_img(self):
        filename = "%s/Anno/list_attr_img.txt" % self.root
        f = open(filename)
        # Skip the first two lines.
        num_files = int(f.readline())
        self.num_files = num_files
        self.filenames = [None]*num_files
        self.attrs = [None]*num_files
        f.readline()
        # Process line-by-line.
        i = 0
        for line in f:
            line = line.rstrip().split()
            filename = line[0].replace("img/", "")
            attr = [elem.replace("-1", "0") for elem in line[1::]]
            attr = torch.LongTensor([float(x) for x in attr])
            self.filenames[i] = filename
            self.attrs[i] = attr
            i += 1
        f.close()

    def get_list_category_img(self):
        filename = "%s/Anno/list_category_img.txt" % self.root
        f = open(filename)
        # Skip the first two lines.
        num_files = int(f.readline())
        self.categories = [None]*num_files
        f.readline()
        # Process line-by-line.
        i = 0
        for line in f:
            line = line.rstrip().split()
            filename = line[0].replace("img/", "")
            category = int(line[-1])
            self.categories[i] = category
            i += 1
        f.close()

    def __getitem__(self, index):
        filepath = "%s/Img/img_converted/%s" % (root, self.filenames[index])
        img = self.transform(Image.open(filepath))
        attr_label = self.attrs[index]
        category_label = self.categories[index]
        return img, category_label, attr_label

    def __len__(self):
        return self.num_files

if __name__ == '__main__':
    from torch.utils.data import DataLoader
    root = os.environ["DEEPFASHION_FOLDER"]
    train_transforms = [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ]
    ds = DeepFashionDataset(root, transforms_=train_transforms)
    loader = DataLoader(ds, batch_size=10, shuffle=False)
    stuff = iter(loader).next()    
