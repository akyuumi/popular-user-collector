import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from controller.main_controller import MainController
import tkinter
from tkinter import filedialog, messagebox, scrolledtext

class ContactCollectorApp:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("連絡先収集アプリ")
        self.root.geometry("500x500")
        self.main_controller = MainController()
        self.create_widgets()

    def create_widgets(self):
        # プルダウンを追加
        options = ["Youtube", "Instagram", "TikTok", "X"]
        self.selected = tkinter.StringVar()
        self.selected.set(options[0])
        self.dropdown = tkinter.OptionMenu(self.root, self.selected, *options)
        self.dropdown.config(width=10)
        self.dropdown.pack(pady=20)

        # テキストボックスを追加
        self.text_box = tkinter.Entry(self.root, width=50)
        self.text_box.pack()
        self.text_box.config(bg='gray', readonlybackground='gray')
        self.text_box.config(state='readonly') # 書き込み不可

        # ファイル読み込みボタン
        self.file_select_button = tkinter.Button(self.root, text="ファイル選択", 
            command=lambda: self.main_controller.file_select_button_clicked(self))
        self.file_select_button.pack()

        # テキストエリアとスクロールバーを追加
        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.text_area.config(state='disabled')  # テキストエリアを編集不可に設定
        self.text_area.pack(pady=10)

        # 実行ボタン
        self.exe_button = tkinter.Button(self.root, text="実行", 
            command=lambda: self.main_controller.exe_button_clicked(self))
        self.exe_button.pack(pady=10)

        # ウィンドウを中央に配置
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    app = ContactCollectorApp()
    app.root.mainloop()