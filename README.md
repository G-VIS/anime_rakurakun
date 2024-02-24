# Anime_rakurakun

このツールは実写映像をアニメ化するフローの効率化のために開発されました。社外への公開は禁止としています。

## 使用上の注意

- このツールは社内用に開発されたものです。社外への公開や無断での配布は禁止しています。
- ツールの使用は、著作権法およびその他の関連法規を遵守する範囲内で行ってください。

## セットアップ方法

Anime_rakurakunを使用するには、以下の手順に従ってセットアップを行ってください。

1. まず、プロジェクトのリポジトリをクローンします。

    ```bash
    git clone https://github.com/G-VIS/anime_rakurakun.git
    ```
### Windowsの場合のStep2~3
2. クローンしたフォルダに移動し、`setup.bat`を実行して環境をセットアップします。

    Windowsでの実行例:

    ```bash
    cd anime_rakurakun
    ./setup.bat
    ```

    このステップで、必要なPython環境や依存パッケージがインストールされます。

3. セットアップが完了したら、`VideoDL.bat`を実行してGUIを起動します。

    ```bash
    ./VideoDL.bat
    ```

    GUIを通じて、実写映像のアニメ化プロセスを管理できるようになります。

## Macの場合のStep2~3
2. クローンしたファイルに実行権限を与えます。
   ```bash
    chmod +x setup.sh
    chmod +x setup.sh
    chmod +x setup.sh
   ```

1. setup, update, use
   ターミナルで実行します。
   ```bash
    sh setup.sh
    sh update.sh
    sh VideoDL.sh
   ```
## 使用方法

GUIが起動したら、画面の指示に従って映像ファイルを選択し、変換プロセスを開始してください。

## ライセンス

このプロジェクトは社内専用ツールであり、特定のライセンス条項の下で配布されています。詳細はプロジェクトのライセンスファイルを参照してください。
