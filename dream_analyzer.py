import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def get_dream_summary(dream_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant spécialisé dans l'analyse de rêves. "
                    "Produis un résumé structuré du rêve en identifiant : "
                    "les personnages, les lieux, les objets et les émotions."
                )
            },
            {
                "role": "user",
                "content": dream_text
            }
        ]
    )
    return response.choices[0].message.content


def get_dream_interpretation(dream_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un interprète de rêves expert en psychologie "
                    "symbolique. Génère une interprétation narrative et "
                    "symbolique profonde du rêve décrit."
                )
            },
            {
                "role": "user",
                "content": dream_text
            }
        ]
    )
    return response.choices[0].message.content


def get_image_prompt(dream_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate ONLY an image generation prompt in English. "
                    "No explanation, no sentence, just descriptive words. "
                    "Maximum 15 words."
                )
            },
            {
                "role": "user",
                "content": dream_text
            }
        ]
    )
    return response.choices[0].message.content
