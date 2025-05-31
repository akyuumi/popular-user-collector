from googleapiclient.discovery import build

# APIキーを設定
import os
import sys
API_KEY = os.getenv('API_KEY')

# YouTube APIサービスを構築
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(channel_id):
    # チャンネルのアップロードプレイリストIDを取得
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        print(f'Channel with ID {channel_id} does not exist.')
        return


if __name__ == '__main__':
    # チャンネルIDを指定して動画を取得
    channel_id = 'UC47bNbS2yYfdFFYmsfxazAg'
    get_channel_videos(channel_id)