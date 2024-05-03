import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL

# 動画をダウンロードして保存する関数
def download_video():
    url = url_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid video URL.")
        return

    # フォルダ選択ダイアログを表示
    download_folder = filedialog.askdirectory(title="Select Download Folder")

    if not download_folder:
        return

    try:
        # yt-dlpを使って動画をダウンロード
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during download: {str(e)}")
    finally:
        # ダウンロードが完了したらウィンドウを閉じる
        root.destroy()

# ダウンロードをキャンセルする関数
def cancel_download():
    messagebox.showinfo("Cancel", "Download cancelled.")
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

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel_download)
cancel_button.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()