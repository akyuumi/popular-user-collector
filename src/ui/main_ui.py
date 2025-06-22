import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from controller.main_controller import MainController
import tkinter
from tkinter import filedialog, messagebox, ttk
import tkinter.font

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
        self.root.geometry("500x600")
        self.main_controller = MainController()

        # メインコンテナを作成
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tkinter.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

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

        self.create_main_menu_frame()
        for platform in PlatformConstants.get_all_platforms():
            self.create_platform_frame(platform)
        self.create_batch_youtube_frame()

        self.show_frame("MainMenu")

        # ウィンドウサイズ変更時のイベントをバインド
        self.root.bind('<Configure>', self.on_window_resize)

    def show_frame(self, page_name):
        if page_name == "MainMenu":
            self.root.geometry("500x600")
        else:
            self.root.geometry("1000x600")
        frame = self.frames[page_name]
        frame.tkraise()
        self.center_window()

    def create_main_menu_frame(self):
        main_menu_frame = ttk.Frame(self.container)
        self.frames["MainMenu"] = main_menu_frame
        main_menu_frame.grid(row=0, column=0, sticky="nsew")

        # Define underlined font
        underlined_font = tkinter.font.Font(size=10, underline=True)

        # --- Online Section ---
        online_container = ttk.Frame(main_menu_frame)
        online_container.pack(pady=(20, 10), padx=20, fill="x")
        
        online_title = ttk.Label(online_container, text="オンライン", font=underlined_font)
        online_title.pack(anchor="w")

        online_frame = ttk.Labelframe(online_container, text="")
        online_frame.pack(pady=5, fill="x", expand=True)

        platforms = PlatformConstants.get_all_platforms()
        num_platforms = len(platforms)

        for i, platform in enumerate(platforms):
            button = ttk.Button(online_frame, text=platform, width=15,
                                  command=lambda p=platform: self.show_frame(p))
            
            row = i // 2
            col = i % 2
            columnspan = 1
            sticky = 'ew'

            button.grid(row=row, column=col, columnspan=columnspan, padx=10, pady=5, ipady=5, sticky=sticky)

        online_frame.grid_columnconfigure(0, weight=1)
        online_frame.grid_columnconfigure(1, weight=1)
        
        # --- Batch Section ---
        batch_container = ttk.Frame(main_menu_frame)
        batch_container.pack(pady=20, padx=10, fill="x")

        batch_title = ttk.Label(batch_container, text="バッチ", font=underlined_font)
        batch_title.pack(anchor="w")

        batch_frame = ttk.Labelframe(batch_container, text="")
        batch_frame.pack(pady=5, fill="x", expand=True)

        for i, platform in enumerate(platforms):
            is_youtube_batch = (platform == PlatformConstants.YOUTUBE)
            btn_state = "normal" if is_youtube_batch else "disabled"
            btn_command = (lambda: self.show_frame("BatchYoutube")) if is_youtube_batch else None
            
            button = ttk.Button(batch_frame, text=platform, width=15, state=btn_state, command=btn_command)
            
            row = i // 2
            col = i % 2
            columnspan = 1
            sticky = 'ew'

            button.grid(row=row, column=col, columnspan=columnspan, padx=10, pady=5, ipady=5, sticky=sticky)

        batch_frame.grid_columnconfigure(0, weight=1)
        batch_frame.grid_columnconfigure(1, weight=1)

    def create_batch_youtube_frame(self):
        frame_name = "BatchYoutube"
        batch_youtube_frame = ttk.Frame(self.container)
        self.frames[frame_name] = batch_youtube_frame
        batch_youtube_frame.grid(row=0, column=0, sticky='nsew')
        batch_youtube_frame.grid_rowconfigure(2, weight=1)
        batch_youtube_frame.grid_columnconfigure(0, weight=1)

        # Top buttons
        back_button = ttk.Button(batch_youtube_frame, text="メニューに戻る", width=15,
                                 command=lambda: self.show_frame("MainMenu"))
        back_button.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")

        get_files_button = ttk.Button(batch_youtube_frame, text="ファイル取得", width=15,
                                      command=lambda: self.main_controller.get_gcs_files_button_clicked(batch_youtube_frame))
        get_files_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        # Listbox with Scrollbar
        listbox_frame = ttk.Frame(batch_youtube_frame)
        listbox_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        batch_youtube_frame.file_listbox = tkinter.Listbox(listbox_frame, selectmode=tkinter.MULTIPLE)
        batch_youtube_frame.file_listbox.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=batch_youtube_frame.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        batch_youtube_frame.file_listbox.config(yscrollcommand=scrollbar.set)

        # Bottom button
        export_button = ttk.Button(batch_youtube_frame, text="出力", width=15,
                                   command=lambda: self.main_controller.export_gcs_file_button_clicked(batch_youtube_frame))
        export_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="e")

    def create_platform_frame(self, platform):
        platform_frame = ttk.Frame(self.container)
        self.frames[platform] = platform_frame
        platform_frame.grid(row=0, column=0, sticky='nsew')
        platform_frame.grid_rowconfigure(5, weight=1)
        platform_frame.grid_columnconfigure(0, weight=1)

        # 戻るボタン
        back_button = ttk.Button(platform_frame, text="メニューに戻る",
                                 command=lambda: self.show_frame("MainMenu"))
        back_button.grid(row=0, column=0, sticky='w', padx=20, pady=10)

        # 検索対象ユーザー用のフレーム
        search_user_frame = ttk.Frame(platform_frame)
        search_user_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 5))

        # 検索対象ユーザーラベル
        search_user_label = ttk.Label(search_user_frame, text="検索対象ユーザー", anchor='w', width=15)
        search_user_label.pack(side=tkinter.TOP, anchor='w')

        # 検索対象ユーザー用テキストボックス
        platform_frame.search_user_text_box = ttk.Entry(search_user_frame, width=30)
        platform_frame.search_user_text_box.pack(side=tkinter.TOP, anchor='w', pady=(5, 0))

        # 検索対象リスト用のフレーム
        search_list_frame = ttk.Frame(platform_frame)
        search_list_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 5))

        # 検索対象リストラベル
        search_list_label = ttk.Label(search_list_frame, text="検索対象リスト", anchor='w', width=15)
        search_list_label.pack(side=tkinter.LEFT)

        # 検索対象リスト用のファイル選択ボタン
        search_list_select_button = tkinter.Button(search_list_frame, text="ファイル選択",
            command=lambda: self.main_controller.search_list_file_select_button_clicked(platform_frame))
        search_list_select_button.pack(side=tkinter.LEFT, padx=(10, 0))

        # 検索対象リスト用テキストボックス
        platform_frame.search_list_text_box = ttk.Entry(platform_frame, width=50)
        platform_frame.search_list_text_box.grid(row=3, column=0, sticky='ew', padx=20)
        platform_frame.search_list_text_box.config(state='readonly') # 書き込み不可

        # ボタンフレーム
        button_frame = ttk.Frame(platform_frame)
        button_frame.grid(row=4, column=0, pady=10)

        # 実行ボタン
        exe_button = tkinter.Button(button_frame, text="実行",
            command=lambda: self.main_controller.exe_button_clicked(platform_frame, platform))
        exe_button.pack(side=tkinter.LEFT, padx=5)

        # 出力ボタン
        export_button = tkinter.Button(button_frame, text="出力",
            command=lambda: self.main_controller.export_button_clicked(platform_frame))
        export_button.pack(side=tkinter.LEFT, padx=5)

        # クリアボタン
        clear_button = tkinter.Button(button_frame, text="クリア",
            command=lambda: self.clear_all(platform_frame))
        clear_button.pack(side=tkinter.LEFT, padx=5)

        # テーブル（Treeview）を追加
        self.create_table_for_platform(platform_frame, platform)

    def clear_all(self, platform_frame):
        # テキストボックスをクリア
        platform_frame.search_user_text_box.delete(0, tkinter.END)

        platform_frame.search_list_text_box.config(state='normal')
        platform_frame.search_list_text_box.delete(0, tkinter.END)
        platform_frame.search_list_text_box.config(state='readonly')

        # テーブルをクリア
        for item in platform_frame.tree.get_children():
            platform_frame.tree.delete(item)

    def create_table_for_platform(self, platform_frame, platform):
        # テーブルとスクロールバーを格納するフレームを作成
        table_frame = ttk.Frame(platform_frame)
        table_frame.grid(row=5, column=0, sticky='nsew', padx=20, pady=20)

        columns = self.table_columns[platform]['columns']
        
        # テーブルを作成
        platform_frame.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # カラムの設定
        for col in columns:
            platform_frame.tree.heading(col, text=self.table_columns[platform]['headings'][col])
            platform_frame.tree.column(col, width=self.table_columns[platform]['widths'][col])

        # スクロールバーを追加
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tkinter.VERTICAL, command=platform_frame.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tkinter.HORIZONTAL, command=platform_frame.tree.xview)
        platform_frame.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # テーブルとスクロールバーを配置
        platform_frame.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        # グリッドの重みを設定
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

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