# Speak with eSpeak-ng

import subprocess

def speak(text):
    """ Speak the given text
    """
    if not text:
        print("No text to speak.")
        return
    print(f"Ollama says: {text}")

    # Use eSpeak-ng to speak the text
    subprocess.run(['espeak-ng', text])

speak("Hello, this is a test of the TTS engine.")