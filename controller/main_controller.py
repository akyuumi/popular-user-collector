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
        
        if selected == "Youtube":
            self.display_youtube_data(app)
        elif selected == "Instagram":
            messagebox.showinfo("Error", "まだ実装されていません。")
        elif selected == "TikTok":
            messagebox.showinfo("Error", "まだ実装されていません。")
        elif selected == "X":
            messagebox.showinfo("Error", "まだ実装されていません。")

    def display_youtube_data(self, app):
        # テキストエリアを編集可能に一時的に変更
        app.text_area.config(state='normal')
        
        # テキストエリアをクリア
        app.text_area.delete(1.0, tkinter.END)
        
        # APIキーチェック
        if not YOUTUBE_API_KEY:
            messagebox.showinfo("Error", "APIキーが設定されていません。")
            return
        
        # テスト用のチャンネルID（例：Google Japan）
        channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'
        channel = get_channel_videos(channel_id)
        
        # チャンネル情報を表示
        app.text_area.insert(tkinter.END, 
            f"チャンネル情報:\n"
            f"タイトル: {channel['title']}\n"
            f"公開日付: {channel['publishedAt']}\n"
            f"購読者数: {channel['subscriberCount']}\n"
            f"動画本数: {channel['videoCount']}\n"
            f"視聴回数: {channel['viewCount']}\n"
            f"説明: {channel['description']}\n"
            f"{'='*80}\n"
        )

        # スクロールを最上部に戻す
        app.text_area.see(1.0)
        
        # テキストエリアを再度編集不可に設定
        app.text_area.config(state='disabled')