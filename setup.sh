#!/bin/bash
echo "Verifying Python installation..."

# Pythonがインストールされているか確認
if ! command -v python &> /dev/null; then
    echo "Python is not installed or not in the PATH."
    exit 1
fi

echo "Python installation found."

# FFmpegがインストールされているか確認
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed or not in the PATH."
    echo "Please download FFmpeg from https://ffmpeg.org/download.html"
    exit 1
fi

echo "FFmpeg installation found."

# 仮想環境のディレクトリ名を指定
VENV_DIR="venv"

# 仮想環境が既に存在するか確認し、存在しない場合は作成
if [ ! -d "$VENV_DIR/bin" ]; then
    echo "Creating virtual environment..."
    python -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# 仮想環境をアクティベート
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# requirements.txtが存在するか確認し、存在する場合は依存関係をインストール
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

echo "Setup complete! Your environment is ready."
read -p "Press [Enter] key to close..."

