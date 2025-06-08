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
print(f"Ollama response: {response}")   