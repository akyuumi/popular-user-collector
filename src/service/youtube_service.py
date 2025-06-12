from tkinter import messagebox
from googleapiclient.discovery import build
import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY

def get_channel_videos(search_user_text_box):
    """
    チャンネル名からチャンネル情報を取得する（曖昧検索対応）
    
    Args:
        search_user_text_box (str): YouTubeチャンネル名（部分一致可）
        
    Returns:
        dict: チャンネル情報
    """
    if not YOUTUBE_API_KEY:
        raise ValueError("APIキーが設定されていません。")
        
    try:
        # APIキーを使用してYouTube APIクライアントを初期化
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # チャンネル名で検索
        search_response = youtube.search().list(
            q=search_user_text_box,
            type='channel',
            part='id',
            maxResults=1
        ).execute()
        
        if not search_response.get('items'):
            raise Exception(f"チャンネルが見つかりませんでした。: {search_user_text_box}")
            
        channel_id = search_response['items'][0]['id']['channelId']
        
        # チャンネルIDを使用してチャンネル情報を取得
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        
        if not response.get('items'):
            raise Exception(f"チャンネル情報の取得に失敗しました。: {channel_id}")
            
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
        if not YOUTUBE_API_KEY:
            messagebox.showerror("Error", "APIキーが設定されていません。")
        elif not response.get('items'):
            messagebox.showerror("Error", f"チャンネルが見つかりませんでした。: {search_user_text_box}")
        else:
            messagebox.showerror("Error", f"YouTube情報取得に失敗しました。: {e}")
        return None
