!/bin/bash
# if not exists:
if [ ! -d "vosk-model-small-en-us-0.15" ]; then
  echo "Vosk model directory does not exist. Downloading..."
  wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
  unzip vosk-model-small-en-us-0.15.zip
else
  echo "Vosk model directory already exists."

fi

echo "Vosk model downloaded and extracted."
echo "installong PortAudio dependencies..."
sudo apt update
sudo apt install libportaudio2 portaudio19-dev -y
