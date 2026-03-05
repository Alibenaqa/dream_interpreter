# Documentation complète — Interprète de Rêves

---

## Introduction

Ce projet est un interprète de rêves intelligent. L'utilisateur décrit son rêve (en texte ou en audio), et l'application génère un résumé, une interprétation symbolique et une image illustrant le rêve.

**Technologies utilisées :**
- **Groq** : héberge le modèle de langage (llama-3.3-70b-versatile) et le modèle de transcription audio (Whisper large-v3, créé par OpenAI)
- **Hugging Face** : héberge le modèle de génération d'images (Stable Diffusion XL, créé par Stability AI)
- **Streamlit** : crée l'interface web
- **python-dotenv** : gère les clés API secrètes
- **requests** : envoie des requêtes HTTP vers Hugging Face

---

## Fichier 1 : requirements.txt

```
groq
streamlit
python-dotenv
requests
```

Ce fichier liste toutes les bibliothèques Python dont le projet a besoin. La commande `pip install -r requirements.txt` les installe toutes en une seule fois.

- `groq` : la bibliothèque officielle pour parler à l'API Groq (LLM + Whisper)
- `streamlit` : crée l'interface web sans avoir besoin de HTML/CSS/JS
- `python-dotenv` : lit le fichier .env pour charger les clés API
- `requests` : envoie des requêtes HTTP (utilisé pour Hugging Face)

---

## Fichier 2 : .env

```
GROQ_API_KEY=ta_cle_groq
HF_TOKEN=ton_token_hugging_face
```

Ce fichier contient les clés API secrètes. Il n'est jamais envoyé sur GitHub grâce au .gitignore. Chaque service (Groq, Hugging Face) donne une clé unique pour identifier qui fait les appels.

---

## Fichier 3 : dream_analyzer.py

Ce fichier contient toutes les fonctions qui utilisent le modèle de langage Groq pour analyser les rêves.

```python
import os
```
Importe le module `os` qui permet de lire les variables d'environnement (les clés dans le fichier .env).

```python
from groq import Groq
```
Importe la classe `Groq` depuis la bibliothèque groq. C'est ce qui nous permet de parler à l'API Groq.

```python
from dotenv import load_dotenv
```
Importe la fonction `load_dotenv` qui lit le fichier .env et charge les variables dedans.

```python
load_dotenv()
```
Exécute la lecture du fichier .env. Après cette ligne, `os.getenv("GROQ_API_KEY")` fonctionne.

```python
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```
Crée une connexion avec l'API Groq en utilisant notre clé secrète. `client` est l'objet qu'on utilisera pour faire tous les appels.

```python
MODEL = "llama-3.3-70b-versatile"
```
Stocke le nom du modèle dans une constante (en majuscules par convention PEP 8). C'est le modèle de langage qu'on utilise — 70 milliards de paramètres, très performant.

---

### Fonction get_dream_summary(dream_text)

```python
def get_dream_summary(dream_text):
```
Définit une fonction qui reçoit le texte du rêve en paramètre.

```python
    response = client.chat.completions.create(
        model=MODEL,
```
Fait un appel à l'API Groq. On utilise `client.chat.completions.create` — c'est le même format que l'API OpenAI (Groq est compatible).

```python
        messages=[
            {"role": "system", "content": "Tu es un assistant spécialisé dans l'analyse de rêves. Produis un résumé structuré du rêve en identifiant : les personnages, les lieux, les objets et les émotions."},
            {"role": "user", "content": dream_text}
        ]
```
On envoie deux messages : le message `system` donne les instructions au modèle (son rôle), le message `user` contient le rêve de l'utilisateur. C'est comme avoir une conversation avec le modèle.

```python
    return response.choices[0].message.content
```
L'API renvoie un objet complexe. On accède à la réponse via `.choices[0].message.content` — c'est le texte généré par le modèle.

---

### Fonction get_dream_interpretation(dream_text)

Même structure que `get_dream_summary` mais avec un prompt système différent : le modèle joue le rôle d'un interprète expert en psychologie symbolique et génère une interprétation narrative profonde.

---

### Fonction get_image_prompt(dream_text)

```python
{"role": "system", "content": "Generate ONLY an image generation prompt in English. No explanation, no sentence, just descriptive words. Maximum 15 words."}
```
On demande au modèle de générer UNIQUEMENT un prompt en anglais, court (max 15 mots), sans phrases. C'est parce que les modèles de génération d'images fonctionnent mieux avec des mots-clés en anglais qu'avec des phrases complètes en français.

---

## Fichier 4 : speech_to_text.py

Ce fichier contient la fonction de transcription audio — transformer un enregistrement vocal en texte.

```python
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```
Même initialisation que dans dream_analyzer.py — on charge les variables d'environnement et on crée le client Groq.

---

### Fonction transcribe_audio(audio_file)

```python
def transcribe_audio(audio_file):
```
Reçoit un fichier audio (capturé par Streamlit via le microphone).

```python
    audio_bytes = audio_file.read()
```
Lit le contenu binaire du fichier audio. `.read()` transforme le fichier en une suite d'octets (bytes).

```python
    transcription = client.audio.transcriptions.create(
        file=("audio.webm", audio_bytes),
```
Envoie le fichier audio à l'API Groq. On précise le nom `"audio.webm"` pour que Groq sache quel format il reçoit. Groq fait tourner **Whisper large-v3** (créé par OpenAI) sur ses serveurs pour faire la transcription.

```python
        model="whisper-large-v3",
```
Spécifie le modèle de transcription. Whisper large-v3 supporte plus de 50 langues dont le français.

```python
        language="fr",
```
Précise explicitement que la langue est le français. Cela améliore la précision de la transcription.

```python
    return transcription.text
```
Retourne le texte transcrit.

---

## Fichier 5 : image_generator.py

Ce fichier contient la fonction qui génère une image à partir d'un texte (text-to-image).

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
```
Imports standards. On utilise `requests` ici (pas la bibliothèque Groq) car Hugging Face n'a pas de bibliothèque Python dédiée — on fait des appels HTTP directs.

```python
HF_API_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)
```
L'URL des serveurs Hugging Face. Le modèle est `stable-diffusion-xl-base-1.0` créé par Stability AI. HF l'héberge sur ses serveurs. L'URL est coupée en deux lignes pour respecter la limite de 79 caractères (règle PEP 8).

---

### Fonction generate_dream_image(image_prompt)

```python
def generate_dream_image(image_prompt):
```
Reçoit le prompt texte (les mots-clés générés par `get_image_prompt`).

```python
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
```
Prépare l'en-tête d'authentification. `Bearer` c'est un standard HTTP pour transmettre un token d'accès. Hugging Face vérifie ce token pour autoriser l'appel.

```python
    clean_prompt = image_prompt.strip().rstrip(".,!?")[:200]
```
Nettoie le prompt en trois étapes :
- `.strip()` : enlève les espaces au début et à la fin
- `.rstrip(".,!?")` : enlève la ponctuation à la fin
- `[:200]` : coupe à 200 caractères maximum

C'est nécessaire car Groq renvoyait parfois des prompts trop longs avec de la ponctuation.

```python
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": clean_prompt},
        timeout=60
    )
```
Envoie une requête POST à Hugging Face. `json={"inputs": clean_prompt}` envoie le prompt au format JSON. `timeout=60` signifie qu'on attend maximum 60 secondes (la génération d'image prend du temps).

```python
    if response.status_code == 200:
        return response.content
    return None
```
Si le serveur répond avec le code 200 (succès), on retourne les bytes de l'image directement. Si ça a raté, on retourne `None` et l'app affichera un avertissement.

---

## Fichier 6 : dream_journal.py

Ce fichier gère la sauvegarde et le chargement des rêves dans un fichier JSON local.

```python
import json
```
Module Python intégré pour lire et écrire du JSON (JavaScript Object Notation) — un format texte pour stocker des données structurées.

```python
import os
```
Pour vérifier si le fichier JSON existe.

```python
from datetime import datetime
```
Pour ajouter la date et l'heure à chaque rêve sauvegardé.

```python
JOURNAL_FILE = "dreams.json"
```
Le nom du fichier de sauvegarde. Constante en majuscules (convention PEP 8).

---

### Fonction save_dream(dream_data)

```python
def save_dream(dream_data):
```
Reçoit un dictionnaire avec le texte du rêve, le résumé, l'interprétation et le prompt image.

```python
    dreams = load_dreams()
```
Charge d'abord tous les rêves existants pour ne pas les écraser.

```python
    dream_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
```
Ajoute la date et l'heure actuelles au format "2024-03-15 14:30". `strftime` formate la date selon le pattern donné.

```python
    dreams.append(dream_data)
```
Ajoute le nouveau rêve à la liste existante.

```python
    with open(JOURNAL_FILE, "w", encoding="utf-8") as file:
        json.dump(dreams, file, ensure_ascii=False, indent=2)
```
Ouvre le fichier en mode écriture ("w") et écrit toute la liste en JSON.
- `ensure_ascii=False` : permet les caractères spéciaux (é, à, ê...)
- `indent=2` : indente le JSON pour le rendre lisible
- `with` : ferme automatiquement le fichier après l'écriture

---

### Fonction load_dreams()

```python
def load_dreams():
    if not os.path.exists(JOURNAL_FILE):
        return []
```
Si le fichier n'existe pas encore (premier lancement), retourne une liste vide.

```python
    with open(JOURNAL_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
```
Ouvre le fichier en lecture ("r") et le convertit de JSON en liste Python.

---

## Fichier 7 : app.py

C'est le fichier principal — il crée l'interface web et orchestre tous les autres fichiers.

```python
import streamlit as st
```
Importe Streamlit. Le `as st` est un alias — raccourci pour ne pas écrire `streamlit.` à chaque fois.

```python
from dream_analyzer import (get_dream_summary, get_dream_interpretation, get_image_prompt)
from speech_to_text import transcribe_audio
from image_generator import generate_dream_image
from dream_journal import save_dream
```
Importe toutes les fonctions des autres fichiers. C'est le principe de **modularité** : chaque fichier a une responsabilité unique.

---

### Fonction initialize_session()

```python
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "images" not in st.session_state:
        st.session_state.images = {}
    if "audio_dream" not in st.session_state:
        st.session_state.audio_dream = None
```
Streamlit recharge le script Python entièrement à chaque interaction. `st.session_state` est la mémoire qui survit entre ces rechargements.

- `messages` : liste de tous les messages de la conversation
- `images` : dictionnaire qui associe chaque message assistant à son image (l'index du message est la clé)
- `audio_dream` : stocke temporairement le texte transcrit depuis le micro

Le `if ... not in` évite d'écraser ces variables à chaque rechargement — on ne les crée qu'une seule fois.

---

### Fonction display_history()

```python
def display_history():
    for i, message in enumerate(st.session_state.messages):
```
`enumerate` donne en même temps l'index `i` et le message. On a besoin de `i` pour retrouver l'image associée.

```python
        with st.chat_message(message["role"]):
```
Crée une bulle de chat. Si `role` est "user" → bulle à droite. Si "assistant" → bulle à gauche avec l'icône robot.

```python
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
```
Affiche le contenu différemment selon qui parle. Pour l'assistant, on affiche résumé, interprétation et image si elle existe.

---

### Fonction analyze_dream(dream_text)

C'est la fonction principale — elle reçoit le texte du rêve et orchestre tout.

```python
    with st.chat_message("user"):
        st.write(dream_text)
    st.session_state.messages.append({"role": "user", "content": dream_text})
```
Affiche le message de l'utilisateur dans le chat et l'ajoute à l'historique.

```python
    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            summary = get_dream_summary(dream_text)
            interpretation = get_dream_interpretation(dream_text)
            image_prompt = get_image_prompt(dream_text)
            image_bytes = generate_dream_image(image_prompt)
```
`st.spinner` affiche une roue de chargement pendant les appels API. Les 4 fonctions s'exécutent dans l'ordre — chacune appelle son API respective.

```python
        st.markdown("**Résumé**")
        st.write(summary)
        st.markdown("**Interprétation**")
        st.write(interpretation)
        if image_bytes:
            st.image(image_bytes)
        else:
            st.warning("L'image n'a pas pu être générée.")
```
Affiche les résultats. Si l'image n'a pas pu être générée (`None`), on affiche un avertissement.

```python
    assistant_index = len(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "summary": summary, "interpretation": interpretation})
    if image_bytes:
        st.session_state.images[assistant_index] = image_bytes
```
On sauvegarde l'index avant d'ajouter le message, puis on stocke l'image avec cet index comme clé. Cela permet à `display_history()` de retrouver l'image au prochain rechargement.

```python
    save_dream({"dream_text": dream_text, "summary": summary, "interpretation": interpretation, "image_prompt": image_prompt})
```
Sauvegarde le rêve dans le fichier JSON local.

---

### Fonction main()

```python
def main():
    st.title("Interprète de Rêves")
    initialize_session()
```
Affiche le titre de la page et initialise la mémoire de session.

```python
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
```
La sidebar (colonne gauche) contient le système audio. `st.audio_input` est le widget microphone. Si l'audio est là et que le bouton est cliqué, on transcrit. `len(cleaned) > 3` évite le bug du silence — Whisper peut halluciner du texte sur un enregistrement silencieux.

```python
    display_history()
```
Affiche tous les messages précédents de la session.

```python
    if st.session_state.audio_dream:
        dream_to_analyze = st.session_state.audio_dream
        st.session_state.audio_dream = None
        analyze_dream(dream_to_analyze)
```
Si un rêve audio a été transcrit, on l'analyse puis on remet `audio_dream` à `None` pour ne pas le ré-analyser au prochain rechargement de Streamlit.

```python
    dream_text = st.chat_input("Décris ton rêve...")
    if dream_text:
        analyze_dream(dream_text)
```
La barre de texte en bas de l'écran. `st.chat_input` attend que l'utilisateur appuie sur Entrée pour envoyer.

```python
if __name__ == "__main__":
    main()
```
Standard Python — si on exécute ce fichier directement, on appelle `main()`. Streamlit vérifie cette condition et l'exécute automatiquement.

---

## Architecture globale

```
app.py  (chef d'orchestre)
  ├── dream_analyzer.py  →  API Groq (LLM llama)
  ├── speech_to_text.py  →  API Groq (Whisper)
  ├── image_generator.py →  API Hugging Face (Stable Diffusion)
  └── dream_journal.py   →  Fichier local dreams.json
```

Chaque fichier a une seule responsabilité — c'est le principe **DRY** (Don't Repeat Yourself) et **KISS** (Keep It Simple, Stupid) appris en cours.
