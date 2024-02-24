#!/bin/bash
# 現在のスクリプトのディレクトリに移動
cd "$(dirname "$0")"
echo "Updating the software..."
# gitを使って最新の状態に更新
git pull

echo "Updating virtual environment..."
# 仮想環境をアクティベート
source venv/bin/activate
# pipをアップグレード
pip install --upgrade pip
# 必要なパッケージをrequirements.txtからインストール
pip install -r requirements.txt
echo "Update complete!"

read -p "Press [Enter] key to close..."