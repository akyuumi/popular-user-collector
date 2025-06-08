import tkinter
from tkinter import filedialog, messagebox
from config import YOUTUBE_API_KEY, INSTAGRAM_ACCESS_TOKEN, X_BEARER_TOKEN
from service.youtube_service import get_channel_videos
from service.instagram_service import get_user_info
from service.x_service import XService

class MainService:
    def __init__(self):
        self.x_service = XService()

    def handle_file_selection(self):
        file_path = filedialog.askopenfilename()
        return file_path if file_path else None

    def handle_youtube_data(self):
        if not YOUTUBE_API_KEY:
            raise ValueError("APIキーが設定されていません。")
        
        channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'  # テスト用のチャンネルID
        return get_channel_videos(channel_id)

    def handle_instagram_data(self):
        if not INSTAGRAM_ACCESS_TOKEN:
            raise ValueError("Instagram APIキーが設定されていません。")
        
        username = 'instagram'  # テスト用のユーザー名
        return get_user_info(username)

    def handle_x_data(self):
        if not X_BEARER_TOKEN:
            raise ValueError("X APIキーが設定されていません。")
        
        username = 'twitter'  # テスト用のユーザー名
        user = self.x_service.get_user_info(username)
        
        if not user:
            raise ValueError("ユーザー情報の取得に失敗しました。")
        
        return user 