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

# GUI setup
root = tk.Tk()
root.title("Video Downloader")

# URL entry
tk.Label(root, text="Enter Video URL:").grid(row=0, column=0, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Save as MP3
mp3_var = tk.BooleanVar()
mp3_check = tk.Checkbutton(root, text="Save as MP3", variable=mp3_var)
mp3_check.grid(row=1, column=0, sticky="e")

# Save as MP4
mp4_var = tk.BooleanVar()
mp4_check = tk.Checkbutton(root, text="Save as MP4", variable=mp4_var)
mp4_check.grid(row=1, column=1, sticky="w")

# File name entry
tk.Label(root, text="Save File As:").grid(row=2, column=0, sticky="e")
file_name_entry = tk.Entry(root, width=50)
file_name_entry.grid(row=2, column=1, padx=5, pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=3, column=0, columnspan=2, pady=5)

# Add the download_for_anime button - Now placed below the Download button
download_for_anime_button = tk.Button(root, text="Download for Anime", command=download_for_anime)
download_for_anime_button.grid(row=4, column=0, columnspan=2, pady=5)  # Adjusted to be on a new line

# The rest of your GUI setup remains unchanged
root.mainloop()
