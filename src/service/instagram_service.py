from tkinter import messagebox
import requests
import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import INSTAGRAM_ACCESS_TOKEN

def get_user_info(username):
    """
    Instagramユーザー名からユーザー情報を取得する
    
    Args:
        username (str): Instagramユーザー名
        
    Returns:
        dict: ユーザー情報
    """
    try:
        # APIキーチェック
        if not INSTAGRAM_ACCESS_TOKEN:
            raise Exception("Instagram APIキーが設定されていません。")

        # Instagram Graph APIのエンドポイント
        url = f"https://graph.instagram.com/v12.0/{username}"
        
        # パラメータの設定
        params = {
            'fields': 'id,username,account_type,media_count',
            'access_token': INSTAGRAM_ACCESS_TOKEN
        }
        
        # APIリクエスト
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        user_data = response.json()
        
        # ユーザー情報を整形
        return {
            'email': '',  # Instagram APIではメールアドレスは取得できない
            'username': user_data.get('username', ''),
            'followers': user_data.get('followers_count', '0'),
            'following': user_data.get('following_count', '0'),
            'posts': user_data.get('media_count', '0'),
            'bio': user_data.get('biography', '')
        }
            
    except Exception as e:
        messagebox.showinfo("Error", f"Instagram情報取得に失敗しました。: {e}")
        raise 