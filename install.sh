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
sudo apt install libportaudio2 portaudio19-dev espeak-ng -y

# Install uv, create virtaul environment and install depenencies
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

echo "Creating virtual environment and installing dependencies..."
if [ ! -d "venv" ]; then
  
  uv venv venv
else
  echo "Virtual environment already exists."
fi
uv pip install -r requirements.txt