import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)


# Génère une image depuis Hugging Face
def generate_dream_image(image_prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
    }
    clean_prompt = image_prompt.strip().rstrip(".,!?")[:200]
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": clean_prompt},
        timeout=60
    )
    if response.status_code == 200:
        return response.content
    return None
