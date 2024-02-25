import tkinter as tk
from tkinter import messagebox, LabelFrame, filedialog
from yt_dlp import YoutubeDL
import os
import subprocess

#ydlを利用してvideoをダウンロードする
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
    with open(settings_path, 'w', encoding='utf-8') as settings_file:
        settings_file.write("フレーム分離・キーフレーム抽出:\n")
        settings_file.write(f"Project_DIR: {project_dir_absolute_path}\n")
        settings_file.write(f"Original_Video: {original_video_path}\n")
        settings_file.write("---------------------------------------------\n\n")

        settings_file.write("タグ付け:\n")
        settings_file.write(f"Key_Dir: {key_dir}\n")
        settings_file.write("---------------------------------------------\n\n")

        settings_file.write("img2imgプロンプト:\n")
        settings_file.write(f"Positive_Prompt_Base: {positive_prompt_base}\n")
        settings_file.write(f"Negative_Prompt_Base: {negative_prompt_base}\n")
        settings_file.write("---------------------------------------------\n\n")

        settings_file.write("画像バッチ処理:\n")
        settings_file.write(f"Key_Dir: {key_dir}\n")
        settings_file.write(f"Img2Img_Key_Dir: {img2img_key_dir}\n")
        settings_file.write("---------------------------------------------\n\n")

        settings_file.write("アップスケール処理:\n")
        settings_file.write(f"Img2Img_Key_Dir: {img2img_key_dir}\n")
        settings_file.write(f"Img2Img_Upscale_Key_Dir: {img2img_upscale_key_dir}\n")
        settings_file.write("---------------------------------------------\n\n")
        
        settings_file.write("ビデオの設定:\n")
        settings_file.write(f"Video URL: {url}\n")
        settings_file.write(f"Format: {format}\n")
        settings_file.write(f"Resolution: {resolution}\n")
        settings_file.write(f"FPS: {fps}\n")
        settings_file.write(f"Codec: {codec}\n")
        settings_file.write("---------------------------------------------\n")


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

        # ユーザーからの入力を取得
        resolution_width = width_entry.get()
        resolution_height = height_entry.get()
        if not resolution_width.isdigit() or not resolution_height.isdigit():
            messagebox.showerror("Error", "Please enter valid numbers for resolution")
            return

        # ffmpegコマンドに解像度を渡す
        scale_option = f'scale={resolution_width}:{resolution_height}'
        subprocess.run([
            'ffmpeg', '-i', input_file, '-vf', scale_option, '-r', '24', 
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', output_file
        ])

        # ユーザーが設定ファイルの作成を選択した場合にのみ、make_settings_file関数を呼び出す
        if create_settings_var.get():
            make_settings_file(
                url=url, 
                file_name=file_name, 
                output_dir=output_dir, 
                format='MP3' if mp3_var.get() else 'MP4', 
                resolution=f'{resolution_width}x{resolution_height}', 
                fps='24', 
                codec='libx264'
            )
        messagebox.showinfo("Success", "Anime style video download and conversion completed")

    download_video_common(url, options, post_download)

# GUI setup
    
root = tk.Tk()
root.title("Video Downloader")

# Main frame-------------
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)
#------------------------

# URL Section------------
url_frame = LabelFrame(main_frame, text="URL")
url_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

url_description_label = tk.Label(url_frame, text="インストールしたい動画のURLを書いてください\n")
url_description_label.pack(side="top", fill="x",)

tk.Label(url_frame, text="Enter Video URL:").pack(side="left")
url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side="left", padx=5)
#------------------------

# Options Section--------
options_frame = LabelFrame(main_frame, text="Options")
options_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

options_description_label = tk.Label(options_frame, text="音だけ保存するならmp3,動画を保存するならmp4を選択\n")
options_description_label.pack(side="top", fill="x",)

mp3_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()
tk.Checkbutton(options_frame, text="Save as MP3", variable=mp3_var).pack(side="left", padx=10)
tk.Checkbutton(options_frame, text="Save as MP4", variable=mp4_var).pack(side="left", padx=10)
#------------------------

# File Name Section------
file_name_frame = LabelFrame(main_frame, text="File Name")
file_name_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

file_description_label = tk.Label(file_name_frame, text="保存するときの名前を決めてください\n")
file_description_label.pack(side="top", fill="x",)

tk.Label(file_name_frame, text="Save File As:").pack(side="left")
file_name_entry = tk.Entry(file_name_frame, width=50)
file_name_entry.pack(side="left", padx=5)
#-----------------------

# Resolution Section----
resolution_frame = LabelFrame(main_frame, text="Resolution")
resolution_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

resolution_description_label = tk.Label(resolution_frame, text="縦動画 : w1080,h1920\n横動画 : w1920,h1080\n")
resolution_description_label.pack(side="top", fill="x",)

tk.Label(resolution_frame, text=" Width:").pack(side="left")
width_entry = tk.Entry(resolution_frame, width=10)
width_entry.pack(side="left", padx=5)
tk.Label(resolution_frame, text=" Height:").pack(side="left")
height_entry = tk.Entry(resolution_frame, width=10)
height_entry.pack(side="left", padx=5)
#------------------------

# Settings File Section--
settings_frame = LabelFrame(main_frame, text="Settings")
settings_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

settings_description_label = tk.Label(settings_frame, text="Ebsynthを使う動画変換をするときはチェックしてください\n")
settings_description_label.pack(side="top", fill="x",)

create_settings_var = tk.BooleanVar()
create_settings_check = tk.Checkbutton(settings_frame, text="Create Settings File", variable=create_settings_var)
create_settings_check.pack(side="left", padx=5)
#------------------------

# Buttons
# download_button = tk.Button(main_frame, text="Download", command=download_video)
# download_button.grid(row=5, column=0, pady=5, sticky="ew")
download_for_anime_button = tk.Button(main_frame, text="Download for Anime", command=download_for_anime)
download_for_anime_button.grid(row=5, column=1, pady=5, sticky="ew")

root.mainloop()

