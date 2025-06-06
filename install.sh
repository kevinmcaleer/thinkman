!/bin/bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

echo "Vosk model downloaded and extracted."
echo "installong PortAudio dependencies..."
sudo apt update
sudo apt install libportaudio2 portaudio19-dev
