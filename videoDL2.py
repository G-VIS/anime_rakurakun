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

def make_settings_file(url, file_name, output_dir, format, resolution, fps, codec):
    """
    Updates the settings.txt file with additional information, including positive and negative prompts.

    Parameters:
    - url: The URL of the video.
    - file_name: The name of the file.
    - output_dir: The directory where the file will be saved.
    - format: The format of the downloaded file (MP3 or MP4).
    - resolution: The resolution of the video after conversion.
    - fps: The frames per second of the video after conversion.
    - codec: The codec used for the video conversion.
    """
    project_dir_absolute_path = os.path.abspath(output_dir)
    original_video_path = os.path.abspath(os.path.join(output_dir, f"{file_name}_anime.mp4"))
    key_dir = os.path.abspath(os.path.join(output_dir, "video_key"))
    img2img_key_dir = os.path.abspath(os.path.join(output_dir, "img2img_key"))
    img2img_upscale_key_dir = os.path.abspath(os.path.join(output_dir, "img2img_upscale_key"))

    positive_prompt_base = "(best quality), (masterpiece), (thighres), illustration, original, extremely detailed wallpaper"
    negative_prompt_base = "(nsfw2), bd,handhvd, rq, degenegative, v1_7k,sketches, (worst quality:2), (low quality:2), (normal quality:2), normal quality, (monochrome), (grayscale), see-through, skin spots, acne, skin blemishes, bad anatomy,DeepNegative, (fa1.2:1), facing away, looking away,tilted head, bad anatomy,bad hands, text, error, missing fingers,extra digits,fewer digits,cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username,blurry, bad feet,cropped, poorly drawn hands,poorly drawn face, mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs, malformed limbs,fused fingers,too many fingers,long neck,cross-eyed, mutated hands, bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra limb, extra leg, extra foot"

    settings_path = os.path.join(output_dir, 'settings.txt')
    with open(settings_path, 'w') as settings_file:
        settings_file.write(f"Project_DIR: {project_dir_absolute_path}\n")
        settings_file.write(f"Original_Video: {original_video_path}\n")
        settings_file.write(f"Key_Dir: {key_dir}\n")
        settings_file.write(f"Img2Img_Key_Dir: {img2img_key_dir}\n")
        settings_file.write(f"Img2Img_Upscale_Key_Dir: {img2img_upscale_key_dir}\n")
        settings_file.write(f"Positive_Prompt_Base: {positive_prompt_base}\n")
        settings_file.write(f"Negative_Prompt_Base: {negative_prompt_base}\n")
        settings_file.write(f"Video URL: {url}\n")
        settings_file.write(f"Format: {format}\n")
        settings_file.write(f"Resolution: {resolution}\n")
        settings_file.write(f"FPS: {fps}\n")
        settings_file.write(f"Codec: {codec}\n")


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

        # Call the make_settings_file function with the appropriate parameters
        make_settings_file(
            url=url, 
            file_name=file_name, 
            output_dir=output_dir, 
            format='MP3' if mp3_var.get() else 'MP4', 
            resolution='1072x1920', 
            fps='24', 
            codec='libx264'
        )
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
