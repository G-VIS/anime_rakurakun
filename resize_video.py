import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def resize_video():
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    # ここで実際のリサイズ処理を行います。ダミーとして、メッセージボックスを表示します。
    messagebox.showinfo("Info", f"Video resized from {input_path} to {output_path}")

# GUIの設定
root = tk.Tk()
root.title("Video Resizer")

# 入力ファイル選択
tk.Label(root, text="Input Video:").grid(row=0, column=0)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2)

# 出力ファイル選択
tk.Label(root, text="Output Video:").grid(row=1, column=0)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2)

# リサイズボタン
tk.Button(root, text="Resize Video", command=resize_video).grid(row=2, column=1)

# GUIの開始
root.mainloop()
