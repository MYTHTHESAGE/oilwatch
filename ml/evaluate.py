import torch
import numpy as np

def calculate_iou(pred_mask, true_mask, threshold=0.5):
    pred_mask = (pred_mask > threshold).float()
    intersection = (pred_mask * true_mask).sum()
    union = pred_mask.sum() + true_mask.sum() - intersection
    if union == 0:
        return 1.0 # Both masks are empty
    return (intersection / union).item()

def evaluate_model(model, dataloader, device):
    model.eval()
    total_iou = 0.0
    with torch.no_grad():
        for inputs, masks in dataloader:
            inputs = inputs.to(device)
            masks = masks.to(device)
            
            outputs = model(inputs)
            total_iou += calculate_iou(outputs, masks)
            
    avg_iou = total_iou / len(dataloader)
    print(f"Average IoU: {avg_iou:.4f}")
    return avg_iou
