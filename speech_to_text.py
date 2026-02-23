import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_file):
    transcription = client.audio.transcriptions.create(
        file=("audio.wav", audio_file.read(), "audio/wav"),
        model="whisper-large-v3",
    )
    return transcription.text
