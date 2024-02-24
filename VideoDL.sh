#!/bin/bash
echo "Activating Python venv environment..."

# 仮想環境のディレクトリを指定
VENV_DIR="venv"

# 仮想環境をアクティベート
source $VENV_DIR/bin/activate

# Pythonスクリプトを実行
python3 videoDL2.py

echo "Application has been executed successfully."
read -p "Press enter to continue"