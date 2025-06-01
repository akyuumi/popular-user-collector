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
    def exe_button_clicked(self, app):
        if not app.text_box.get():
            messagebox.showinfo("Error", "ファイルを選択してください。")
        else:
            self.display_test_data(app)

    def display_test_data(self, app):
        # テキストエリアを編集可能に一時的に変更
        app.text_area.config(state='normal')
        
        # テキストエリアをクリア
        app.text_area.delete(1.0, tkinter.END)
        
        # APIキーチェック
        if not YOUTUBE_API_KEY:
            messagebox.showinfo("Error", "APIキーが設定されていません。")
            return
        
        try:
            # テスト用のチャンネルID（例：Google Japan）
            channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'
            videos = get_channel_videos(channel_id)
            
            # 動画情報を表示
            for i, video in enumerate(videos, 1):
                app.text_area.insert(tkinter.END, 
                    f"動画 {i}:\n"
                    f"タイトル: {video['title']}\n"
                    f"公開日時: {video['publishedAt']}\n"
                    f"説明: {video['description'][:100]}...\n"
                    f"URL: https://www.youtube.com/watch?v={video['videoId']}\n"
                    f"{'='*50}\n"
                )
                
                # 100件で制限
                if i >= 100:
                    break
                    
        except Exception as e:
            messagebox.showinfo("Error", f"YouTube情報取得に失敗しました。: {e}")
            return

        # スクロールを最上部に戻す
        app.text_area.see(1.0)
        
        # テキストエリアを再度編集不可に設定
        app.text_area.config(state='disabled')