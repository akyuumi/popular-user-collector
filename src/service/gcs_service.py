import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from tkinter import messagebox

class GcsService:
    def __init__(self):
        self.credentials = self._get_credentials()
        if self.credentials:
            self.storage_client = storage.Client(credentials=self.credentials)
        else:
            self.storage_client = None

    def _get_credentials(self):
        credentials_json_str = os.environ.get('GCS_CREDENTIALS_JSON')
        if not credentials_json_str:
            messagebox.showerror("エラー", "環境変数 GCS_CREDENTIALS_JSON が設定されていません。")
            return None
        try:
            credentials_info = json.loads(credentials_json_str)
            return service_account.Credentials.from_service_account_info(credentials_info)
        except (json.JSONDecodeError, TypeError) as e:
            messagebox.showerror("エラー", f"GCS認証情報の読み込みに失敗しました: {e}")
            return None

    def list_files(self):
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        if not self.storage_client or not bucket_name:
            if not bucket_name:
                messagebox.showerror("エラー", "環境変数 GCS_BUCKET_NAME が設定されていません。")
            return []
        
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blobs = bucket.list_blobs()
            return [blob.name for blob in blobs]
        except Exception as e:
            messagebox.showerror("エラー", f"GCSからのファイルリスト取得に失敗しました: {e}")
            return []

    def download_file(self, source_blob_name, destination_file_path):
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        if not self.storage_client or not bucket_name:
            if not bucket_name:
                messagebox.showerror("エラー", "環境変数 GCS_BUCKET_NAME が設定されていません。")
            return False

        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_path)
            return True
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルのダウンロードに失敗しました: {e}")
            return False 