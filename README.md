# Interprète Intelligent de Rêves

Application interactive qui analyse et interprète les rêves décrits par l'utilisateur,
génère une interprétation symbolique et une illustration visuelle, et conserve un journal
des rêves.

---

## Technologies utilisées

| Outil | Rôle |
|---|---|
| Python | Langage principal |
| Groq (llama-3.3-70b-versatile) | Résumé et interprétation du rêve |
| Groq (whisper-large-v3) | Transcription audio en texte |
| Hugging Face (stable-diffusion-xl) | Génération d'image |
| Streamlit | Interface web interactive |
| python-dotenv | Gestion sécurisée des clés API |

---

## Structure du projet

```
dream_interpreter/
├── app.py                # Interface Streamlit principale
├── dream_analyzer.py     # Appels au LLM Groq (résumé, interprétation, prompt image)
├── speech_to_text.py     # Transcription audio avec Groq Whisper
├── image_generator.py    # Génération d'image avec Hugging Face
├── dream_journal.py      # Sauvegarde et chargement du journal (JSON)
├── requirements.txt      # Bibliothèques nécessaires
└── .env                  # Clés API (non versionné)
```

---

## Installation et lancement

### 1. Cloner le projet
```
git clone <url-du-repo>
cd dream_interpreter
```

### 2. Créer et activer l'environnement virtuel
```
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```
pip install -r requirements.txt
```

### 4. Configurer les clés API

Créer un fichier `.env` à la racine :
```
GROQ_API_KEY=votre_clé_groq
HF_TOKEN=votre_token_huggingface
```

- Clé Groq : https://console.groq.com
- Token Hugging Face : https://huggingface.co/settings/tokens

### 5. Lancer l'application
```
streamlit run app.py
```

---

## Fonctionnalités

- Saisie du rêve par texte ou enregistrement audio
- Résumé structuré (personnages, lieux, émotions)
- Interprétation symbolique et narrative générée par IA
- Illustration visuelle du rêve générée automatiquement
- Journal consultable des rêves précédents

---

## Jeu de prompts documenté

### Prompt 1 — Résumé structuré (`get_dream_summary`)

```
Rôle system : "Tu es un assistant spécialisé dans l'analyse de rêves.
Produis un résumé structuré du rêve en identifiant :
les personnages, les lieux, les objets et les émotions."
```

**Objectif** : Extraire les éléments clés du rêve de façon organisée.
**Choix** : Un rôle spécialisé pousse le modèle à structurer sa réponse
plutôt que de raconter librement.

---

### Prompt 2 — Interprétation symbolique (`get_dream_interpretation`)

```
Rôle system : "Tu es un interprète de rêves expert en psychologie
symbolique. Génère une interprétation narrative et symbolique
profonde du rêve décrit."
```

**Objectif** : Produire une analyse psychologique et symbolique du rêve.
**Choix** : Le rôle d'expert oriente le modèle vers une interprétation
profonde plutôt qu'une simple description.

---

### Prompt 3 — Prompt visuel (`get_image_prompt`)

```
Rôle system : "Generate ONLY an image generation prompt in English.
No explanation, no sentence, just descriptive words.
Maximum 15 words."
```

**Objectif** : Générer un prompt court et visuel pour le modèle de
génération d'images.
**Choix** : La contrainte "ONLY" et "just descriptive words" est
indispensable — sans elle, le modèle renvoie une phrase complète
qui casse l'URL ou dépasse la limite du modèle image.

---

## Difficultés rencontrées

### 1. Pollinations.ai inaccessible
L'API de génération d'images Pollinations.ai retournait une erreur
**1033 (Cloudflare Access Denied)** depuis notre réseau.
**Solution** : Migration vers l'API Hugging Face Inference avec le
modèle `stable-diffusion-xl-base-1.0`.

### 2. Changement d'URL de l'API Hugging Face
L'ancienne URL `api-inference.huggingface.co` retournait une erreur
**410 Gone** — l'API a migré vers une nouvelle adresse.
**Solution** : Utilisation de la nouvelle URL
`router.huggingface.co/hf-inference/models/...`.

### 3. Prompt image trop long
Sans contrainte stricte sur le prompt visuel, Groq renvoyait une
phrase complète (ex: "Here is a prompt: ...") qui causait des erreurs
lors de l'appel à l'API image.
**Solution** : Ajout de la contrainte "Maximum 15 words" et
"just descriptive words" dans le system prompt, et troncature
à 200 caractères dans le code.
