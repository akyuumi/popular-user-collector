import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from tkinter import messagebox
import tempfile
import pandas as pd

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

    def get_csv_file_blob(self):
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        if not self.storage_client or not bucket_name:
            if not bucket_name:
                messagebox.showerror("エラー", "環境変数 GCS_BUCKET_NAME が設定されていません。")
            return None
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blobs = list(bucket.list_blobs(prefix="csv/"))
            csv_blobs = [blob for blob in blobs if blob.name.endswith('.csv') and not blob.name.endswith('/')]
            if not csv_blobs:
                messagebox.showinfo("情報", "/csv配下にCSVファイルが見つかりません。")
                return None
            return csv_blobs[0]  # 1ファイル前提
        except Exception as e:
            messagebox.showerror("エラー", f"GCSからのCSVファイル取得に失敗しました: {e}")
            return None

    def download_and_read_csv(self):
        blob = self.get_csv_file_blob()
        if not blob:
            return None, None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                blob.download_to_filename(tmp_file.name)
                df = pd.read_csv(tmp_file.name)
            return df, blob.name
        except Exception as e:
            messagebox.showerror("エラー", f"CSVファイルのダウンロードまたは読込に失敗しました: {e}")
            return None, None

    def download_csv_to(self, destination_file_path):
        blob = self.get_csv_file_blob()
        if not blob:
            return False
        try:
            blob.download_to_filename(destination_file_path)
            return True
        except Exception as e:
            messagebox.showerror("エラー", f"CSVファイルのダウンロードに失敗しました: {e}")
            return False 