import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter
from tkinter import filedialog, messagebox

from config import YOUTUBE_API_KEY, INSTAGRAM_ACCESS_TOKEN, X_BEARER_TOKEN
from service.youtube_service import get_channel_videos
from service.instagram_service import get_user_info
from service.x_service import XService

class MainController:

    def __init__(self):
        self.x_service = XService()

    # ファイル選択ボタンクリック
    def file_select_button_clicked(self, app):
        file_path = filedialog.askopenfilename()
        if file_path:
            app.template_text_box.config(state='normal')
            app.template_text_box.delete(0, tkinter.END)
            app.template_text_box.insert(0, file_path)
            app.template_text_box.config(state='readonly')

    # 実行ボタンクリック
    def exe_button_clicked(self, app, selected):
        # テンプレートファイルが選択されていない場合はエラー
        # if not app.template_text_box.get():
        #     messagebox.showinfo("Error", "ファイルを選択してください。")
        #     return
        
        if selected == "Youtube":
            self.display_youtube_data(app)
        elif selected == "Instagram":
            self.display_instagram_data(app)
        elif selected == "TikTok":
            messagebox.showinfo("Error", "まだ実装されていません。")
        elif selected == "X":
            self.display_x_data(app)

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
            '',  # email field (empty)
            channel['title'],
            channel['publishedAt'],
            channel['subscriberCount'],
            channel['videoCount'],
            channel['viewCount'],
            channel['description']
        ))

    def display_instagram_data(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # APIキーチェック
        if not INSTAGRAM_ACCESS_TOKEN:
            messagebox.showinfo("Error", "Instagram APIキーが設定されていません。")
            return
        
        # テスト用のユーザー名（例：instagram）
        username = 'instagram'
        user = get_user_info(username)
        
        # ユーザー情報をテーブルに追加
        app.tree.insert('', 'end', values=(
            user['email'],
            user['username'],
            user['followers'],
            user['following'],
            user['posts'],
            user['bio']
        ))

    def display_x_data(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # APIキーチェック
        if not X_BEARER_TOKEN:
            messagebox.showinfo("Error", "X APIキーが設定されていません。")
            return
        
        # テスト用のユーザー名（例：twitter）
        username = 'twitter'
        user = self.x_service.get_user_info(username)
        
        if not user:
            messagebox.showinfo("Error", "ユーザー情報の取得に失敗しました。")
            return
        
        # ユーザー情報をテーブルに追加
        app.tree.insert('', 'end', values=(
            '',  # email field (empty)
            user['username'],
            user['followers'],
            user['following'],
            user['tweets'],
            user['bio']
        ))