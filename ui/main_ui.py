import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from controller.main_controller import MainController
import tkinter
from tkinter import filedialog, messagebox, ttk

class ContactCollectorApp:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("連絡先収集アプリ")
        self.root.geometry("1000x600")
        self.main_controller = MainController()
        
        # メインフレームを作成
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.create_widgets()
        
        # ウィンドウサイズ変更時のイベントをバインド
        self.root.bind('<Configure>', self.on_window_resize)

    def create_widgets(self):
        # プルダウンを追加
        options = ["Youtube", "Instagram", "TikTok", "X"]
        self.selected = tkinter.StringVar()
        self.selected.set(options[0])
        self.dropdown = tkinter.OptionMenu(self.main_frame, self.selected, *options)
        self.dropdown.config(width=10)
        self.dropdown.pack(pady=20)

        # テキストボックスを追加
        self.text_box = tkinter.Entry(self.main_frame, width=50)
        self.text_box.pack(fill=tkinter.X, padx=20)
        self.text_box.config(bg='gray', readonlybackground='gray')
        self.text_box.config(state='readonly') # 書き込み不可

        # ファイル読み込みボタン
        self.file_select_button = tkinter.Button(self.main_frame, text="ファイル選択", 
            command=lambda: self.main_controller.file_select_button_clicked(self))
        self.file_select_button.pack(pady=10)

        # テーブル（Treeview）を追加
        self.tree = ttk.Treeview(self.main_frame, columns=('title', 'publishedAt', 'subscriberCount', 'videoCount', 'viewCount', 'description'), show='headings')
        
        # カラムの設定
        self.tree.heading('title', text='タイトル')
        self.tree.heading('publishedAt', text='公開日付')
        self.tree.heading('subscriberCount', text='登録者数')
        self.tree.heading('videoCount', text='動画本数')
        self.tree.heading('viewCount', text='視聴回数')
        self.tree.heading('description', text='チャンネル説明')
        
        # カラムの幅を設定
        self.tree.column('title', width=200)
        self.tree.column('publishedAt', width=150)
        self.tree.column('subscriberCount', width=100)
        self.tree.column('videoCount', width=100)
        self.tree.column('viewCount', width=100)
        self.tree.column('description', width=300)
        
        # スクロールバーを追加
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # テーブルとスクロールバーを配置
        self.tree.pack(fill=tkinter.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # 実行ボタン
        self.exe_button = tkinter.Button(self.main_frame, text="実行", 
            command=lambda: self.main_controller.exe_button_clicked(self, self.selected.get()))
        self.exe_button.pack(after=self.tree, pady=10)

        # ウィンドウを中央に配置
        self.center_window()

    def on_window_resize(self, event):
        # ウィンドウサイズが変更された時の処理
        if event.widget == self.root:
            # テーブルは自動的にリサイズされるため、
            # 特別な処理は不要
            pass

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    app = ContactCollectorApp()
    app.root.mainloop()