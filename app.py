import streamlit as st
from dream_analyzer import (
    get_dream_summary,
    get_dream_interpretation,
    get_image_prompt
)
from speech_to_text import transcribe_audio
from image_generator import generate_dream_image
from dream_journal import save_dream, load_dreams


def main():
    st.title("Interprète de Rêves")

    st.subheader("Décris ton rêve")

    input_method = st.radio(
        "Comment veux-tu décrire ton rêve ?",
        ["Texte", "Audio"]
    )

    dream_text = ""

    if input_method == "Texte":
        dream_text = st.text_area("Écris ton rêve ici...")

    else:
        audio_file = st.audio_input("Enregistre ton rêve")
        if audio_file:
            with st.spinner("Transcription en cours..."):
                dream_text = transcribe_audio(audio_file)
            st.write("**Transcription :**", dream_text)

    if st.button("Analyser mon rêve") and dream_text:
        with st.spinner("Analyse en cours..."):
            summary = get_dream_summary(dream_text)
            interpretation = get_dream_interpretation(dream_text)
            image_prompt = get_image_prompt(dream_text)
            image_bytes = generate_dream_image(image_prompt)

        st.subheader("Résumé")
        st.write(summary)

        st.subheader("Interprétation")
        st.write(interpretation)

        st.subheader("Illustration du rêve")
        if image_bytes:
            st.image(image_bytes)
        else:
            st.warning("L'image n'a pas pu être générée.")

        dream_data = {
            "dream_text": dream_text,
            "summary": summary,
            "interpretation": interpretation,
            "image_prompt": image_prompt,
        }
        save_dream(dream_data)
        st.success("Rêve sauvegardé dans ton journal !")

    st.divider()
    st.subheader("Journal des rêves")

    dreams = load_dreams()

    if not dreams:
        st.write("Aucun rêve enregistré pour l'instant.")
    else:
        for dream in reversed(dreams):
            with st.expander(f"Rêve du {dream['date']}"):
                st.write("**Texte original :**", dream["dream_text"])
                st.write("**Résumé :**", dream["summary"])
                st.write("**Interprétation :**", dream["interpretation"])


if __name__ == "__main__":
    main()
