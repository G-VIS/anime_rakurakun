import os
import subprocess
import tkinter as tk
from tkinter import messagebox, LabelFrame, filedialog
from yt_dlp import YoutubeDL
"""
Convert YouTube subtitles(vtt) to human readable text.
Download only subtitles from YouTube with youtube-dl:
youtube-dl  --skip-download --convert-subs vtt <video_url>
Note that default subtitle format provided by YouTube is ass, which is hard
to process with simple regex. Luckily youtube-dl can convert ass to vtt, which
is easier to process.
To conver all vtt files inside a directory:
find . -name "*.vtt" -exec python vtt2text.py {} \;
"""
import sys
import re


def remove_tags(text):
    """
    Remove vtt markup tags
    """
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',

    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    # extract timestamp, only kep HH:MM
    text = re.sub(
        r'(\d{2}:\d{2}):\d{2}\.\d{3} --> .* align:start position:0%',
        r'\g<1>',
        text
    )

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text

def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in ('##', 'Language: en',):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match('^\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            yield '\n' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer


def convert_vtt_to_text(vtt_file_path):
    txt_name =  re.sub(r'.vtt$', '.txt', vtt_file_path)
    with open(vtt_file_path, encoding='utf-8') as f:
        text = f.read()
    text = remove_tags(text)
    lines = text.splitlines()
    lines = remove_header(lines)
    lines = merge_duplicates(lines)
    lines = list(lines)
    lines = merge_short_lines(lines)
    lines = list(lines)

    with open(txt_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            f.write("\n")


# 動画をダウンロードして保存する関数
def download_script():
    # 保存先フォルダpath
    download_folder = f"C:/Users/eleph/OneDrive/デスクトップ/downloads"
    url = url_entry.get()
    # 指定されたフォルダがなければ作成
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # 選択された言語に基づいて字幕の言語を設定
    sub_lang = lang_var.get()

    # yt-dlpを使って字幕をダウンロード
    command = f'yt-dlp --write-auto-sub --skip-download --sub-lang {sub_lang} --output "{download_folder}/%(title)s.%(ext)s" {url}'
    subprocess.run(command, shell=True)
    
    # ダウンロードしたファイルの名前を取得するための仮の方法
    # 実際には、フォルダ内の最新の.vttファイルを検索するなどの方法が考えられます
    # ここでは、yt-dlpの出力からファイル名を正確に取得する方法を実装する必要があります
    vtt_files = [f for f in os.listdir(download_folder) if f.endswith('.vtt')]
    if vtt_files:
        # 最新のファイルを選択
        vtt_file_path = os.path.join(download_folder, sorted(vtt_files)[-1])
        print(vtt_file_path)
        # VTTファイルをテキストに変換
        convert_vtt_to_text(vtt_file_path)
    else:
        print("ダウンロードしたVTTファイルが見つかりません。")

    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Video Downloader")

# URL Section------------
tk.Label(root, text="Enter Video URL:").grid(row=0, column=0, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
#------------------------

# Options Section--------
options_frame = LabelFrame(root, text="Options")
options_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

options_description_label = tk.Label(options_frame, text="字幕の言語を選択\n")
options_description_label.pack(side="top", fill="x",)

# StringVarを使用して選択された言語を保持
lang_var = tk.StringVar()
lang_var.set("ja")  # default

# Radiobuttonを使用して、jaかenのどちらか一方を選択
tk.Radiobutton(options_frame, text="Save as Japanese", variable=lang_var, value="ja").pack(side="left", padx=10)
tk.Radiobutton(options_frame, text="Save as English", variable=lang_var, value="en").pack(side="left", padx=10)
#------------------------

# Download button
download_button = tk.Button(root, text="Download", command=download_script)
download_button.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
