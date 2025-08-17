import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import torchvision.transforms as transforms

def base64_to_tensor(base64_str):
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[-1]

    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data)).convert("L")
    except UnidentifiedImageError:
        raise ValueError("Cannot recognize, please check if the format is base64")
    except Exception as e:
        raise ValueError(f"Decode Base64 error：{str(e)}")

    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    return transform(image).unsqueeze(0)