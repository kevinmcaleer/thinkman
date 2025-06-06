# Thinkman - an offline Raspberry Pi AI assistant

## pre-requisites

In order to run this project, you need to have a Raspberry Pi with Raspberry Pi OS installed. You also need to have Python 3 installed on your Raspberry Pi.

```bash
uv pip install vosk sounddevice pyttsx3 requests
```

Install the Vosk model for English:

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```
