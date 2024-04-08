@echo off
echo Activating Python venv environment...

:: 仮想環境のディレクトリを指定
set VENV_DIR=venv

:: 仮想環境をアクティベート
call %VENV_DIR%\Scripts\activate

:: Pythonスクリプトを実行
python video_download.py

echo Application has been executed successfully.
exit
