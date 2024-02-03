import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
import os
import subprocess

def download_video_common(url, options, post_download_action=None):
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    if post_download_action:
        post_download_action()

def download_video():
    url = url_entry.get()
    save_as_mp3 = mp3_var.get()
    save_as_mp4 = mp4_var.get()
    file_name = file_name_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    if not (save_as_mp3 or save_as_mp4):
        messagebox.showerror("Error", "Please select a format to save the file")
        return

    options = {
        'outtmpl': f'../downloads/{file_name}.%(ext)s',
        'format': 'bestaudio/best' if save_as_mp3 else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if save_as_mp3 else [],
    }

    download_video_common(url, options, lambda: messagebox.showinfo("Success", "Download completed"))

def download_for_anime():
    url = url_entry.get()
    file_name = file_name_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    options = {
        'outtmpl': f'../downloads/{file_name}/{file_name}.%(ext)s',
        'format': 'best',
    }

    def post_download():
        output_dir = f'../downloads/{file_name}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for folder in ['img2img_key', 'img2img_upscale_key']:
            if not os.path.exists(f'{output_dir}/{folder}'):
                os.makedirs(f'{output_dir}/{folder}')
        input_file = f'{output_dir}/{file_name}.mp4'
        output_file = f'{output_dir}/{file_name}_anime.mp4'
        subprocess.run([
            'ffmpeg', '-i', input_file, '-vf', 'scale=1072:1920', '-r', '24', 
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', output_file
        ])
        messagebox.showinfo("Success", "Anime style video download and conversion completed")

    download_video_common(url, options, post_download)

# GUI setup continues as before
# Add the download_for_anime button
download_for_anime_button = tk.Button(root, text="Download for Anime", command=download_for_anime)
download_for_anime_button.grid(row=3, column=1, pady=5)

# The rest of your GUI setup remains unchanged
