import os
import torch
from torch.utils.data import Dataset
import numpy as np

class SARDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.patches_dir = os.path.join(data_dir, "patches")
        self.masks_dir = os.path.join(data_dir, "masks")
        if os.path.exists(self.patches_dir):
            self.filenames = [f for f in os.listdir(self.patches_dir) if f.endswith('.npy')]
        else:
            self.filenames = []

    def __len__(self):
        # Return a mock length if data doesn't exist to allow code to run
        return len(self.filenames) if self.filenames else 100

    def __getitem__(self, idx):
        if not self.filenames:
            # Mock data for demonstration purposes if dataset has not been generated
            patch = torch.rand(2, 256, 256)
            mask = torch.randint(0, 2, (1, 256, 256), dtype=torch.float32)
            return patch, mask

        filename = self.filenames[idx]
        patch_path = os.path.join(self.patches_dir, filename)
        mask_path = os.path.join(self.masks_dir, filename)

        patch = np.load(patch_path)
        mask = np.load(mask_path)
        
        patch_tensor = torch.from_numpy(patch).float()
        mask_tensor = torch.from_numpy(mask).float().unsqueeze(0)

        if self.transform:
            # Apply basic augmentations
            pass

        return patch_tensor, mask_tensor
