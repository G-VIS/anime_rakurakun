@echo off
echo Verifying Python installation...

:: Pythonがインストールされているか確認
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in the PATH.
    exit /b 1
)

echo Python installation found.

:: FFmpegがインストールされているか確認
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg is not installed or not in the PATH.
    echo Please download FFmpeg from https://ffmpeg.org/download.html
    exit /b 1
)

echo FFmpeg installation found.

:: 仮想環境のディレクトリ名を指定
set VENV_DIR=venv

:: 仮想環境が既に存在するか確認し、存在しない場合は作成
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
) else (
    echo Virtual environment already exists.
)

:: 仮想環境をアクティベート
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate

:: requirements.txtが存在するか確認し、存在する場合は依存関係をインストール
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

echo Setup complete! Your environment is ready.
pause