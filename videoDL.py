import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL

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

    with YoutubeDL(options) as ydl:
        ydl.download([url])

    messagebox.showinfo("Success", "Download completed")

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

root.mainloop()
