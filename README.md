# OBLO
An AI generated clown, with animated ascii, that runs in a terminal window

# Oblo - A AI Clown Voice Assistant

Please welcome **Oblo**, your very own strange, secretive, and slightly unhinged clown assistant. Oblo listens, responds, and even plays games with you using voice interaction. This project combines speech recognition, text-to-speech, rich terminal interfaces, and a dash of generative AI for a unique voice assistant experience that runs purely in terminal.

---

## 🔄 Features

- **Voice Recognition:** Uses [Vosk](https://alphacephei.com/vosk/) to transcribe your voice in real time
- **Text-to-Speech (TTS):** Replies out loud using `pyttsx3`
- **Gemini Integration:** AI responses are generated with Google's Gemini API
- **Terminal UI:** Rich-styled output using the `rich` library
- **Character Personality:** Oblo is not just a voice assistant—he has lore, secrets, and an attitude

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/oblo.git
cd oblo
```

### 2. Set Up Your Environment
It's recommended to use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Your API Key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your-api-key-here
```

---

## 🧩 Technologies Used
- `vosk` - Offline voice recognition
- `pyttsx3` - Offline TTS engine
- `google-generativeai` - Gemini API integration
- `rich` - Beautiful terminal output
- `sounddevice` - Audio stream handling
- `python-dotenv` - Load API keys and secrets

---

## ⚒️ Contributing
Want to add new games, features, or clown behaviors? Fork the repo and go wild!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add something'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

---

## 🌈 Oblo's Lore
> "I've always been Oblo, here to cheer you up and maintain that pep in your step... or have I.."

Talk to Oblo. Trust him... or don't.

---

## 🌐 License
MIT License. See [LICENSE](LICENSE) file for details.

---

Enjoy Oblo — your eerie, eccentric assistant who may or may not remember what you said last time...

🎈🎩🕵️‍♂️

