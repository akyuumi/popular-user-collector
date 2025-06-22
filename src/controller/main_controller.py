import sys
import os
import pandas as pd

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter
from tkinter import filedialog, messagebox

from config import INSTAGRAM_ACCESS_TOKEN, X_BEARER_TOKEN
from service.main_service import MainService
from service.gcs_service import GcsService

class MainController:

    def __init__(self):
        self.main_service = MainService()
        self.gcs_service = GcsService()

    # 検索対象リスト用のファイル選択ボタンクリック
    def search_list_file_select_button_clicked(self, platform_frame):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            platform_frame.search_list_text_box.config(state='normal')
            platform_frame.search_list_text_box.delete(0, 'end')
            platform_frame.search_list_text_box.insert(0, file_path)
            platform_frame.search_list_text_box.config(state='readonly')
            messagebox.showinfo("完了", "テーブルに出力しました。")
        else:
            messagebox.showerror("エラー", "データがありません。")

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
            elif selected == "テスト":
                self._handle_test_execution(app)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_youtube_execution(self, app):
        
        search_user_text_box: str = app.search_user_text_box.get()
        search_list_text_box: str = app.search_list_text_box.get()

        if search_user_text_box:
            # 単一ユーザーの場合
            channel = self.main_service.handle_youtube_data(search_user_text_box)
            if channel:
                app.tree.insert('', 'end', values=(
                    channel['email'],
                    channel['title'],
                    channel['publishedAt'],
                    channel['subscriberCount'],
                    channel['videoCount'],
                    channel['viewCount'],
                    channel['description']
                ))
        elif search_list_text_box:
            # ファイルから複数ユーザーを読み込む場合
            try:
                with open(search_list_text_box, 'r', encoding='utf-8') as file:
                    for line in file:
                        username = line.strip()
                        if username:  # 空行をスキップ
                            channel = self.main_service.handle_youtube_data(username)
                            if channel:
                                app.tree.insert('', 'end', values=(
                                    channel['email'],
                                    channel['title'],
                                    channel['publishedAt'],
                                    channel['subscriberCount'],
                                    channel['videoCount'],
                                    channel['viewCount'],
                                    channel['description']
                                ))
            except Exception as e:
                messagebox.showerror("Error", f"ファイルの読み込み中にエラーが発生しました: {e}")
        else:
            messagebox.showinfo("Info", "検索対象ユーザーまたは検索対象リストを入力してください。")

    def _handle_instagram_execution(self, app):
        
        # APIキーチェック
        if not INSTAGRAM_ACCESS_TOKEN:
            messagebox.showinfo("Error", "Instagram APIキーが設定されていません。")
            return
        
        # サービス呼び出し
        user = self.main_service.handle_instagram_data()
        
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
        
        # APIキーチェック
        if not X_BEARER_TOKEN:
            messagebox.showinfo("Error", "X APIキーが設定されていません。")
            return
        
        # サービス呼び出し
        user = self.main_service.handle_x_data()
        
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

    def _handle_test_execution(self, app):
        
        # テストデータを取得
        test_data = self.main_service.handle_test_data()
        
        # テストデータをテーブルに追加
        for data in test_data:
            app.tree.insert('', 'end', values=(
                data['email'],
                data['title'],
                data['publishedAt'],
                data['subscriberCount'],
                data['videoCount'],
                data['viewCount'],
                data['description']
            ))

    def export_button_clicked(self, app):
        """
        テーブルの内容をCSVファイルとして出力する
        
        Args:
            app: アプリケーションインスタンス
        """
        try:
            # ファイル保存ダイアログを表示
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="CSVファイルの保存"
            )
            
            if not file_path:  # キャンセルされた場合
                return
                
            # 現在選択されているプラットフォームのカラム設定を取得
            platform = app.selected.get()
            columns = app.table_columns[platform]['columns']
            headings = app.table_columns[platform]['headings']
            
            # CSVファイルに書き込み
            with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                # ヘッダー行を書き込み
                header = [headings[col] for col in columns]
                f.write(','.join(header) + '\n')
                
                # データ行を書き込み
                for item in app.tree.get_children():
                    values = app.tree.item(item)['values']
                    # カンマを含む値をダブルクォートで囲む
                    row = []
                    for value in values:
                        if isinstance(value, str) and ',' in value:
                            row.append(f'"{value}"')
                        else:
                            row.append(str(value))
                    f.write(','.join(row) + '\n')
                    
            messagebox.showinfo("成功", "CSVファイルの出力が完了しました。")
            
        except Exception as e:
            messagebox.showerror("エラー", f"CSVファイルの出力に失敗しました: {str(e)}")

    def get_gcs_files_button_clicked(self, batch_youtube_frame):
        file_list = self.gcs_service.list_files()
        
        batch_youtube_frame.file_listbox.delete(0, 'end')

        if file_list:
            for file_name in file_list:
                batch_youtube_frame.file_listbox.insert('end', file_name)
        else:
            messagebox.showinfo("情報", "GCSにファイルが見つかりません。")

    def export_gcs_file_button_clicked(self, batch_youtube_frame):
        selected_indices = batch_youtube_frame.file_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("警告", "ファイルが選択されていません。")
            return

        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return

        success_count = 0
        for i in selected_indices:
            file_name = batch_youtube_frame.file_listbox.get(i)
            destination_path = os.path.join(folder_selected, file_name)
            if self.gcs_service.download_file(file_name, destination_path):
                success_count += 1
        
        if success_count > 0:
            messagebox.showinfo("完了", f"{success_count}個のファイルのダウンロードが完了しました。")