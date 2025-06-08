import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter
from tkinter import filedialog, messagebox

from config import INSTAGRAM_ACCESS_TOKEN, X_BEARER_TOKEN
from service.main_service import MainService

class MainController:

    def __init__(self):
        self.service = MainService()

    # ファイル選択ボタンクリック
    def file_select_button_clicked(self, app):
        try:
            file_path = self.service.handle_file_selection()
            if file_path:
                app.template_text_box.config(state='normal')
                app.template_text_box.delete(0, 'end')
                app.template_text_box.insert(0, file_path)
                app.template_text_box.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 実行ボタンクリック
    def exe_button_clicked(self, app, selected):
        try:
            # テーブルをクリア
            for item in app.tree.get_children():
                app.tree.delete(item)

            if selected == "Youtube":
                self._handle_youtube_execution(app)
            elif selected == "Instagram":
                self._handle_instagram_execution(app)
            elif selected == "TikTok":
                messagebox.showinfo("Info", "まだ実装されていません。")
            elif selected == "X":
                self._handle_x_execution(app)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_youtube_execution(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # テスト用のチャンネルID（例：Google Japan）
        channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'
        channel = self.service.handle_youtube_data()
        
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

    def _handle_instagram_execution(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # APIキーチェック
        if not INSTAGRAM_ACCESS_TOKEN:
            messagebox.showinfo("Error", "Instagram APIキーが設定されていません。")
            return
        
        # テスト用のユーザー名（例：instagram）
        username = 'instagram'
        user = self.service.handle_instagram_data()
        
        # ユーザー情報をテーブルに追加
        app.tree.insert('', 'end', values=(
            user['email'],
            user['username'],
            user['followers'],
            user['following'],
            user['posts'],
            user['bio']
        ))

    def _handle_x_execution(self, app):
        # テーブルをクリア
        for item in app.tree.get_children():
            app.tree.delete(item)
        
        # APIキーチェック
        if not X_BEARER_TOKEN:
            messagebox.showinfo("Error", "X APIキーが設定されていません。")
            return
        
        # テスト用のユーザー名（例：twitter）
        username = 'twitter'
        user = self.service.handle_x_data()
        
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