import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from controller.main_controller import MainController
import tkinter
from tkinter import filedialog, messagebox, ttk

class PlatformConstants:
    YOUTUBE = "Youtube"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    X = "X"
    TEST = "テスト"

    @classmethod
    def get_all_platforms(cls):
        return [cls.YOUTUBE, cls.INSTAGRAM, cls.TIKTOK, cls.X, cls.TEST]

class ContactCollectorApp:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("アドレスコレクター")
        self.root.geometry("1000x600")
        self.main_controller = MainController()
        
        # メインフレームを作成
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)
        
        # テーブルカラム定義
        self.table_columns = {
            PlatformConstants.YOUTUBE: {
                'columns': ('email', 'title', 'publishedAt', 'subscriberCount', 'videoCount', 'viewCount', 'description'),
                'headings': {
                    'email': 'メールアドレス',
                    'title': 'タイトル',
                    'publishedAt': '公開日付',
                    'subscriberCount': '登録者数',
                    'videoCount': '動画本数',
                    'viewCount': '視聴回数',
                    'description': 'チャンネル説明'
                },
                'widths': {
                    'email': 200,
                    'title': 200,
                    'publishedAt': 150,
                    'subscriberCount': 100,
                    'videoCount': 100,
                    'viewCount': 100,
                    'description': 300
                }
            },
            PlatformConstants.TEST: {
                'columns': ('email', 'title', 'publishedAt', 'subscriberCount', 'videoCount', 'viewCount', 'description'),
                'headings': {
                    'email': 'メールアドレス',
                    'title': 'タイトル',
                    'publishedAt': '公開日付',
                    'subscriberCount': '登録者数',
                    'videoCount': '動画本数',
                    'viewCount': '視聴回数',
                    'description': 'チャンネル説明'
                },
                'widths': {
                    'email': 200,
                    'title': 200,
                    'publishedAt': 150,
                    'subscriberCount': 100,
                    'videoCount': 100,
                    'viewCount': 100,
                    'description': 300
                }
            },
            PlatformConstants.INSTAGRAM: {
                'columns': ('email', 'username', 'followers', 'following', 'posts', 'bio'),
                'headings': {
                    'email': 'メールアドレス',
                    'username': 'ユーザー名',
                    'followers': 'フォロワー数',
                    'following': 'フォロー数',
                    'posts': '投稿数',
                    'bio': 'プロフィール'
                },
                'widths': {
                    'email': 200,
                    'username': 150,
                    'followers': 100,
                    'following': 100,
                    'posts': 100,
                    'bio': 400
                }
            },
            PlatformConstants.TIKTOK: {
                'columns': ('email', 'username', 'followers', 'following', 'likes', 'bio'),
                'headings': {
                    'email': 'メールアドレス',
                    'username': 'ユーザー名',
                    'followers': 'フォロワー数',
                    'following': 'フォロー数',
                    'likes': 'いいね数',
                    'bio': 'プロフィール'
                },
                'widths': {
                    'email': 200,
                    'username': 150,
                    'followers': 100,
                    'following': 100,
                    'likes': 100,
                    'bio': 400
                }
            },
            PlatformConstants.X: {
                'columns': ('email', 'username', 'followers', 'following', 'tweets', 'bio'),
                'headings': {
                    'email': 'メールアドレス',
                    'username': 'ユーザー名',
                    'followers': 'フォロワー数',
                    'following': 'フォロー数',
                    'tweets': 'ツイート数',
                    'bio': 'プロフィール'
                },
                'widths': {
                    'email': 200,
                    'username': 150,
                    'followers': 100,
                    'following': 100,
                    'tweets': 100,
                    'bio': 400
                }
            }
        }
        
        self.create_widgets()
        
        # ウィンドウサイズ変更時のイベントをバインド
        self.root.bind('<Configure>', self.on_window_resize)

    def create_widgets(self):
        # 上部フレーム（プルダウン用）
        top_frame = ttk.Frame(self.main_frame)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        
        # プルダウンを追加
        self.selected = tkinter.StringVar()
        self.selected.set(PlatformConstants.YOUTUBE)
        self.dropdown = tkinter.OptionMenu(top_frame, self.selected, *PlatformConstants.get_all_platforms(), 
            command=self.update_table_columns)
        self.dropdown.config(width=10)
        self.dropdown.pack(expand=True)

        # 検索対象ユーザー用のフレーム
        search_user_frame = ttk.Frame(self.main_frame)
        search_user_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 5))
        
        # 検索対象ユーザーラベル
        search_user_label = ttk.Label(search_user_frame, text="検索対象ユーザー", anchor='w', width=15)
        search_user_label.pack(side=tkinter.TOP, anchor='w')
        
        # 検索対象ユーザー用テキストボックス
        self.search_user_text_box = ttk.Entry(search_user_frame, width=30)
        self.search_user_text_box.pack(side=tkinter.TOP, anchor='w', pady=(5, 0))

        # 検索対象リスト用のフレーム
        search_list_frame = ttk.Frame(self.main_frame)
        search_list_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 5))
        
        # 検索対象リストラベル
        search_list_label = ttk.Label(search_list_frame, text="検索対象リスト", anchor='w', width=15)
        search_list_label.pack(side=tkinter.LEFT)
        
        # 検索対象リスト用のファイル選択ボタン
        self.search_list_select_button = tkinter.Button(search_list_frame, text="ファイル選択",
            command=lambda: self.main_controller.search_list_file_select_button_clicked(self))
        self.search_list_select_button.pack(side=tkinter.LEFT, padx=(10, 0))

        # 検索対象リスト用テキストボックス
        self.search_list_text_box = ttk.Entry(self.main_frame, width=50)
        self.search_list_text_box.grid(row=3, column=0, sticky='ew', padx=20)
        self.search_list_text_box.config(state='readonly') # 書き込み不可

        # テンプレートファイル用のフレーム
        template_frame = ttk.Frame(self.main_frame)
        template_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=(0, 5))
        
        # テンプレートファイルラベル
        template_label = ttk.Label(template_frame, text="テンプレートファイル", anchor='w', width=15)
        template_label.pack(side=tkinter.LEFT)
        
        # テンプレート用のファイル選択ボタン
        self.template_select_button = tkinter.Button(template_frame, text="ファイル選択",
            command=lambda: self.main_controller.template_file_select_button_clicked(self))
        self.template_select_button.pack(side=tkinter.LEFT, padx=(10, 0))

        # テンプレート用のファイル出力ボタン
        self.template_output_button = tkinter.Button(template_frame, text="ファイル出力",
            command=lambda: self.main_controller.file_output_button_clicked(self))
        self.template_output_button.pack(side=tkinter.LEFT, padx=(10, 0))

        # テンプレート用テキストボックス
        self.template_text_box = ttk.Entry(self.main_frame, width=50)
        self.template_text_box.grid(row=5, column=0, sticky='ew', padx=20)
        self.template_text_box.config(state='readonly') # 書き込み不可

        # ボタンフレーム
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=6, column=0, pady=10)

        # 実行ボタン
        self.exe_button = tkinter.Button(button_frame, text="実行", 
            command=lambda: self.main_controller.exe_button_clicked(self, self.selected.get()))
        self.exe_button.pack(side=tkinter.LEFT, padx=5)

        # クリアボタン
        self.clear_button = tkinter.Button(button_frame, text="クリア",
            command=self.clear_all)
        self.clear_button.pack(side=tkinter.LEFT, padx=5)

        # テーブル（Treeview）を追加
        self.create_table()

        # ウィンドウを中央に配置
        self.center_window()

        # メインフレームのグリッド設定
        self.main_frame.grid_rowconfigure(7, weight=1)  # テーブル行に重みを設定
        self.main_frame.grid_columnconfigure(0, weight=1)  # 列に重みを設定

    def clear_all(self):
        # テキストボックスをクリア
        self.search_user_text_box.delete(0, tkinter.END)

        self.search_list_text_box.config(state='normal')
        self.search_list_text_box.delete(0, tkinter.END)
        self.search_list_text_box.config(state='readonly')

        self.template_text_box.config(state='normal')
        self.template_text_box.delete(0, tkinter.END)
        self.template_text_box.config(state='readonly')

        # テーブルをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)

    def create_table(self):
        # 既存のテーブルがある場合は削除
        if hasattr(self, 'tree'):
            self.tree.destroy()
            self.scrollbar_y.destroy()
            self.scrollbar_x.destroy()

        # 現在選択されているプラットフォームのカラム設定を取得
        platform = self.selected.get()
        columns = self.table_columns[platform]['columns']
        
        # テーブルとスクロールバーを格納するフレームを作成
        table_frame = ttk.Frame(self.main_frame)
        table_frame.grid(row=7, column=0, sticky='nsew', padx=20, pady=20)
        
        # テーブルを作成
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # カラムの設定
        for col in columns:
            self.tree.heading(col, text=self.table_columns[platform]['headings'][col])
            self.tree.column(col, width=self.table_columns[platform]['widths'][col])
        
        # スクロールバーを追加
        self.scrollbar_y = ttk.Scrollbar(table_frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(table_frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        # テーブルとスクロールバーを配置
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # グリッドの重みを設定
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def update_table_columns(self, *args):
        self.create_table()

    def on_window_resize(self, event):
        # ウィンドウサイズが変更された時の処理
        if event.widget == self.root:
            # 特別な処理は不要
            pass

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    app = ContactCollectorApp()
    app.root.mainloop()