import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter
from tkinter import filedialog, messagebox

from config import YOUTUBE_API_KEY
from service.youtube_service import get_channel_videos

class MainController:

    def __init__(self):
        pass

    # ファイル選択ボタンクリック
    def file_select_button_clicked(self, app):
        file_path = filedialog.askopenfilename()
        if file_path:
            app.text_box.config(state='normal')
            app.text_box.delete(0, tkinter.END)
            app.text_box.insert(0, file_path)
            app.text_box.config(state='readonly')

    # 実行ボタンクリック
    def exe_button_clicked(self, app, selected):
        if not app.text_box.get():
            messagebox.showinfo("Error", "ファイルを選択してください。")
            return
        
        if selected == "Youtube":
            self.display_youtube_data(app)
        elif selected == "Instagram":
            messagebox.showinfo("Error", "まだ実装されていません。")
        elif selected == "TikTok":
            messagebox.showinfo("Error", "まだ実装されていません。")
        elif selected == "X":
            messagebox.showinfo("Error", "まだ実装されていません。")

    def display_youtube_data(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # APIキーチェック
        if not YOUTUBE_API_KEY:
            messagebox.showinfo("Error", "APIキーが設定されていません。")
            return
        
        # テスト用のチャンネルID（例：Google Japan）
        channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'
        channel = get_channel_videos(channel_id)
        
        # チャンネル情報をテーブルに追加
        app.tree.insert('', 'end', values=(
            channel['title'],
            channel['publishedAt'],
            channel['subscriberCount'],
            channel['videoCount'],
            channel['viewCount'],
            channel['description']
        ))