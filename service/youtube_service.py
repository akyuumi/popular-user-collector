from tkinter import messagebox
from googleapiclient.discovery import build
import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY

def get_channel_videos(channel_id):
    """
    チャンネルIDからチャンネル情報を取得する
    
    Args:
        channel_id (str): YouTubeチャンネルID
        
    Returns:
        dict: チャンネル情報
    """
    try:
        # APIキーを使用してYouTube APIクライアントを初期化
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # チャンネル情報を取得
        request = youtube.channels().list(
            part="snippet,statistics",
            forUsername="googlejapan"
        )
        response = request.execute()
        
        if not response.get('items'):
            raise Exception("チャンネルが見つかりませんでした。")
            
        channel = response['items'][0]
        channel_data = {
            # タイトル
            'title': channel['snippet']['title'],
            # 説明
            'description': channel['snippet']['description'],
            # 公開日付
            'publishedAt': channel['snippet']['publishedAt'],
            # 登録者数
            'subscriberCount': f"{int(channel['statistics']['subscriberCount']):,}",
            # 動画本数
            'videoCount': f"{int(channel['statistics']['videoCount']):,}",
            # 視聴回数
            'viewCount': f"{int(channel['statistics']['viewCount']):,}",
            # サムネイル
            'thumbnails': channel['snippet']['thumbnails']
        }
            
        return channel_data
        
    except Exception as e:
        messagebox.showinfo("Error", f"YouTube情報取得に失敗しました。: {e}")
        raise
