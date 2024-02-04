@echo off
cd /d %~dp0
echo Updating the software...
git pull

echo Updating virtual environment...
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Update complete!
pause
