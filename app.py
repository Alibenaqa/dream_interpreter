import streamlit as st
from dream_analyzer import (
    get_dream_summary,
    get_dream_interpretation,
    get_image_prompt
)
from speech_to_text import transcribe_audio
from image_generator import generate_dream_image
from dream_journal import save_dream


def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "images" not in st.session_state:
        st.session_state.images = {}
    if "audio_dream" not in st.session_state:
        st.session_state.audio_dream = None


def display_history():
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.write(message["content"])
            else:
                st.markdown("**Résumé**")
                st.write(message["summary"])
                st.markdown("**Interprétation**")
                st.write(message["interpretation"])
                if i in st.session_state.images:
                    st.markdown("**Illustration**")
                    st.image(st.session_state.images[i])


def analyze_dream(dream_text):
    with st.chat_message("user"):
        st.write(dream_text)

    st.session_state.messages.append({
        "role": "user",
        "content": dream_text
    })

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            summary = get_dream_summary(dream_text)
            interpretation = get_dream_interpretation(dream_text)
            image_prompt = get_image_prompt(dream_text)
            image_bytes = generate_dream_image(image_prompt)

        st.markdown("**Résumé**")
        st.write(summary)
        st.markdown("**Interprétation**")
        st.write(interpretation)
        if image_bytes:
            st.markdown("**Illustration**")
            st.image(image_bytes)
        else:
            st.warning("L'image n'a pas pu être générée.")

    assistant_index = len(st.session_state.messages)
    st.session_state.messages.append({
        "role": "assistant",
        "summary": summary,
        "interpretation": interpretation,
    })

    if image_bytes:
        st.session_state.images[assistant_index] = image_bytes

    save_dream({
        "dream_text": dream_text,
        "summary": summary,
        "interpretation": interpretation,
        "image_prompt": image_prompt,
    })


def main():
    st.title("Interprète de Rêves")

    initialize_session()

    with st.sidebar:
        st.header("Enregistrement audio")
        audio_file = st.audio_input("Enregistre ton rêve")
        if audio_file:
            if st.button("Transcrire et analyser"):
                with st.spinner("Transcription en cours..."):
                    transcribed = transcribe_audio(audio_file)
                cleaned = transcribed.strip()
                if len(cleaned) > 3:
                    st.session_state.audio_dream = cleaned
                    st.success(f"Transcrit : {cleaned}")
                else:
                    st.error("Rien n'a été capté. Réessaie.")

    display_history()

    if st.session_state.audio_dream:
        dream_to_analyze = st.session_state.audio_dream
        st.session_state.audio_dream = None
        analyze_dream(dream_to_analyze)

    dream_text = st.chat_input("Décris ton rêve...")
    if dream_text:
        analyze_dream(dream_text)


if __name__ == "__main__":
    main()
