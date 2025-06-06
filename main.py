""" Thinkman - A simple voice assistant using Vosk for speech recognition and Ollama for language generation. """

import queue
from time import sleep
import json
import subprocess
import re
import sounddevice as sd
import vosk
import pyttsx3
import requests
from requests.exceptions import RequestException

PROMPT = "You are a helpful assistant. Answer the user's questions in a friendly and informative manner. "
WELCOME_MESSAGE = "Hello! I am your virtual assistant. How can I help you today?"

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


def clean_response(text):
     # Remove <think>...</think> and normalize whitespace
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)

    # Keep letters, numbers, whitespace, and punctuation (.,!?'"-;:)
    text = re.sub(r"[^a-zA-Z0-9\s\.,!?'\-\":;]", "", text)

    text = remove_emojis(text)
    text = text.replace("*", "")  # Optional, in case * is used for markdown
    return text.strip()


# Set up your paths
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:1.5b"  # or "deepseek-llm:7b" if installed

# Initialize TTS engine
tts = pyttsx3.init()

# Set up Vosk
model = vosk.Model(VOSK_MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    q.put(bytes(indata))

def recognize_speech():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening... Speak a command.")
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
            else:
                pass  # Keep buffering input


def query_ollama(prompt, retries=3, timeout=30):
    print(f"Sending prompt to Ollama: {prompt}")
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }, timeout=timeout)

            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print("Retrying in 2 seconds...")
                sleep(2)
            else:
                return "Sorry, I couldn't get a response from the language model."

# def query_ollama(prompt):
#     print(f"Sending prompt to Ollama: {prompt}")
#     response = requests.post(OLLAMA_URL, json={
#         "model": OLLAMA_MODEL,
#         "prompt": prompt,
#         "stream": False
#     })
#     data = response.json()
#     return data.get("response", "").strip()

def speak(text):
    if not text:
        print("No text to speak.")
        return
    print(f"Ollama says: {text}")

    subprocess.run(['espeak-ng', text])

    # tts.say(text)
    # tts.runAndWait()
    # tts.stop()  # Ensure TTS stops before next input
    # sleep(1)  # Small delay to ensure TTS finishes before next input

def main():
    print("Say something...")
    speak(WELCOME_MESSAGE)
    while True:
        spoken = recognize_speech()
        if not spoken:
            continue
        print(f"You said: {spoken}")
        if spoken.lower() in ["exit", "quit", "stop","bye","goodbye"," good bye"]:
            speak("Goodbye!")
            break
        response = query_ollama(spoken)
        cleaned_response = clean_response(response)
        speak(cleaned_response)

if __name__ == "__main__":
    main()
