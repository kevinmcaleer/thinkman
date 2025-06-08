## Listen with Vosk speech Recognition

import sounddevice as sd
import vosk
import queue
import json

VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"

sentence = ""

# Set up Vosk
model = vosk.Model(VOSK_MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    q.put(bytes(indata))

def recognize_speech():
    """ Recognize speech using Vosk """

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

while True and (sentence not in ["stop","bye", "exit"]):
    sentence = recognize_speech()
    print(f"Recognized: {sentence}")
   