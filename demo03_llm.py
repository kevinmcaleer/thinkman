import queue
import time
import json
import sounddevice as sd
import vosk
import requests
from requests.exceptions import RequestException
import re

VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:1.5b"  # or "deepseek-llm:7b" if installed

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
    text = re.sub(r"\s+", " ", text) # Normalize whitespace

    # Keep letters, numbers, whitespace, and punctuation (.,!?'"-;:)
    text = re.sub(r"[^a-zA-Z0-9\s\.,!?'\-\":;]", "", text)

    text = remove_emojis(text)
    text = text.replace("*", "")  # Optional, in case * is used for markdown
    return text.strip()

def query_ollama(prompt):
    print(f"Sending prompt to Ollama: {prompt}")
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get("response", "").strip()
    except RequestException as e:
        print(f"Error querying Ollama: {e}")
        return ""
    
prompt = "What is the capital of France?"

response = query_ollama(prompt=prompt)
response = clean_response(response)
print(f"Ollama response: {response}")   