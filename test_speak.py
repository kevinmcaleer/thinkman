import subprocess

def speak(text):
    """ Speak the given text using TTS engine. """
    if not text:
        print("No text to speak.")
        return
    print(f"Ollama says: {text}")

    subprocess.run(['espeak-ng', text])

speak("Hello, this is a test of the TTS engine.")