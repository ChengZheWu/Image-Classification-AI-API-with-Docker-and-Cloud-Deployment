from app.utils import base64_to_tensor
from app.model import load_model
import torch

model = load_model()
model.eval()

def predict_digit(base64_img):
    tensor = base64_to_tensor(base64_img)
    with torch.no_grad():
        output = model(tensor)
        _, predicted = torch.max(output.data, 1)
    return int(predicted.item())