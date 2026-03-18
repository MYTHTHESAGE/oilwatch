import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from backend.models.unet import UNet
from ml.dataset import SARDataset
import os

def train_model(epochs=5, batch_size=8, lr=1e-4):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    dataset = SARDataset(data_dir="data")
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = UNet(n_channels=2, n_classes=1).to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    os.makedirs("backend/checkpoints", exist_ok=True)
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        
        for i, (inputs, masks) in enumerate(dataloader):
            inputs = inputs.to(device)
            masks = masks.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(dataloader):.4f}")
        
    print("Training complete. Saving checkpoint to backend/checkpoints/best_model.pth")
    torch.save(model.state_dict(), "backend/checkpoints/best_model.pth")

if __name__ == "__main__":
    # Ensure this can be run as a mock training script
    train_model(epochs=1)
