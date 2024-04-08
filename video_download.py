import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL

# 動画をダウンロードして保存する関数
def download_video():
    # 保存先フォルダpath
    download_folder = f"C:/Users/eleph/OneDrive/デスクトップ/downloads"
    url = url_entry.get()
    # 指定されたフォルダがなければ作成
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # yt-dlpを使って動画をダウンロード
    # ファイル名を動画タイトルに指定し、最高画質の動画と音声を選択して結合し、MP4形式を保証
    command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -o "{download_folder}/%(title)s.%(ext)s" {url}'
    subprocess.run(command, shell=True)
    
    # ダウンロードが完了したらウィンドウを閉じる
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Video Downloader")

# URL entry
tk.Label(root, text="Enter Video URL:").grid(row=0, column=0, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()

