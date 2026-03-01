import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Transcription audio en texte
def transcribe_audio(audio_file):
    audio_bytes = audio_file.read()
    transcription = client.audio.transcriptions.create(
        file=("audio.webm", audio_bytes),
        model="whisper-large-v3",
        language="fr",
    )
    return transcription.text
