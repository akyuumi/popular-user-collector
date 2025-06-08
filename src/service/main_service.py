import tkinter
from tkinter import filedialog, messagebox
from config import YOUTUBE_API_KEY, INSTAGRAM_ACCESS_TOKEN, X_BEARER_TOKEN
from service.youtube_service import get_channel_videos
from service.instagram_service import get_user_info
from service.x_service import XService
import random
import re
from datetime import datetime, timedelta

class MainService:
    def __init__(self):
        self.x_service = XService()

    def handle_file_selection(self):
        file_path = filedialog.askopenfilename()
        return file_path if file_path else None

    def handle_youtube_data(self):
        channel_id = 'UCZf__ehlCEBPop-_sldpBUQ'  # テスト用のチャンネルID
        return get_channel_videos(channel_id)

    def handle_test_data(self):
        test_data = []
        for i in range(100):
            # メールアドレスを含む説明文を生成
            description = f"チャンネル{i}の説明文です。"
            if random.random() < 0.3:  # 30%の確率でメールアドレスを含める
                email = f"test{i}@example.com"
                description += f" お問い合わせは {email} までお願いします。"
            
            # テストデータを生成
            data = {
                'title': f'テストチャンネル {i}',
                'publishedAt': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                'subscriberCount': f"{random.randint(1000, 1000000):,}",
                'videoCount': f"{random.randint(10, 1000):,}",
                'viewCount': f"{random.randint(10000, 10000000):,}",
                'description': description
            }
            
            # メールアドレスを抽出
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', description)
            data['email'] = email_match.group(0) if email_match else ''
            
            test_data.append(data)
        
        return test_data

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