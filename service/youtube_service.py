from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

# APIキーを設定
import os
import sys

def get_channel_videos(channel_id):
    """
    チャンネルIDから動画情報を取得する
    
    Args:
        channel_id (str): YouTubeチャンネルID
        
    Returns:
        list: 動画情報のリスト
    """
    try:
        # APIキーを使用してYouTube APIクライアントを初期化
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # チャンネルの動画を取得
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            type="video"
        )
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'publishedAt': item['snippet']['publishedAt'],
                'videoId': item['id']['videoId']
            }
            videos.append(video_data)
            
        return videos
        
    except Exception as e:
        print(f"Error fetching videos: {str(e)}")
        raise
