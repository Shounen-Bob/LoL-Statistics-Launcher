import tkinter as tk
from tkinter import messagebox
import webbrowser
import re

class Config:
    WINDOW_TITLE = "LoL統計ランチャー"
    WINDOW_SIZE = "250x390"
    BUTTONS = [
        ("SumRift", "https://lolalytics.com/lol/{q}/build/"),
        ("ARAM", "https://lolalytics.com/lol/{q}/aram/build/")
    ]
    LIST_FILE = "champions.txt"

class ChampionSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.resizable(False, True)
        self.root.attributes("-topmost", True)  # 常に最前面に表示
        self.champion_list = self._load_list(Config.LIST_FILE)
        self.filtered_list = self.champion_list
        self.current_index = 0  # 現在の選択インデックスを追跡
        self._setup_widgets()
        self.root.bind("<FocusIn>", self._focus_textbox)

    def _load_list(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            messagebox.showerror(
                "リストファイルが見つかりません",
                f"リストファイル '{file_path}' が見つかりません。\n"
                "以下の手順でファイルを準備してください:\n"
                "1. ファイル名: champions.txt\n"
                "2. 内容: 1行に1チャンピオン名を記載\n\n"
                "例:\nAatrox\nAhri\nAkali\n...\n\n"
                "このアプリと同じフォルダに格納し再起動してください。"
            )
            return []
        except Exception as e:
            messagebox.showerror(
                "エラー",
                f"リストファイルの読み込み中にエラーが発生しました: {e}\n"
                "ファイルの内容や形式を確認してください。"
            )
            return []

    def _setup_widgets(self):
        tk.Label(self.root, text=Config.WINDOW_TITLE, fg="blue", font=("Helvetica", 16, "bold")).pack(pady=5)
        self.entry = self._create_entry()
        tk.Label(self.root, text="↑チャンピオン名(英名)を入力↑", fg="Black", font=("Helvetica", 8)).pack(pady=5)
        self.listbox = self._create_listbox()
        self._create_buttons()
        tk.Label(self.root, text="Enter: サモナーズリフト統計表示\nShift+Enter: ARAM統計表示\n↑↓: カーソル移動", justify="center").pack(pady=5)
        tk.Label(self.root, text="Version 1.0  By 少年ボブ", font=("Helvetica", 10, "italic")).pack(pady=5)

    def _create_entry(self):
        entry = tk.Entry(self.root)
        entry.pack(pady=10)
        entry.bind("<KeyRelease>", self._filter_list)
        entry.bind("<Return>", lambda _: self._search(Config.BUTTONS[0][1]))
        entry.bind("<Shift-Return>", lambda _: self._search(Config.BUTTONS[1][1]))
        entry.bind("<Up>", lambda e: self._move_selection(-1))
        entry.bind("<Down>", lambda e: self._move_selection(1))
        return entry

    def _create_listbox(self):
        listbox = tk.Listbox(self.root, height=5)
        listbox.pack(pady=10, fill="both", expand=True)
        listbox.bind("<Up>", lambda _: self._move_selection(-1))
        listbox.bind("<Down>", lambda _: self._move_selection(1))
        listbox.bind("<Return>", lambda _: self._search(Config.BUTTONS[0][1]))
        listbox.bind("<Shift-Return>", lambda _: self._search(Config.BUTTONS[1][1]))
        return listbox

    def _create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        for text, url in Config.BUTTONS:
            tk.Button(frame, text=text, command=lambda u=url: self._search(u)).pack(side="left", padx=10)
        tk.Button(self.root, text="QUIT", command=self.root.quit).pack(pady=5)

    def _filter_list(self, _):
        query = self.entry.get().strip().lower()
        self.filtered_list = [c for c in self.champion_list if query in c.lower()] if query else self.champion_list
        self._update_listbox()

    def _update_listbox(self):
        self.listbox.delete(0, tk.END)
        for champion in self.filtered_list:
            self.listbox.insert(tk.END, champion)
        if self.filtered_list:
            self.listbox.select_set(self.current_index)
            self.listbox.see(self.current_index)

    def _move_selection(self, direction):
        if not self.filtered_list:
            return

        self.current_index = max(0, min(len(self.filtered_list) - 1, self.current_index + direction))
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(self.current_index)
        self.listbox.see(self.current_index)

    def _search(self, url):
        if not self.filtered_list:
            return

        # アルファベット以外の文字を除外
        champion = re.sub(r"[^a-zA-Z]", "", self.filtered_list[self.current_index]).lower()
        webbrowser.open(url.replace("{q}", champion))

    def _focus_textbox(self, _):
        self.entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChampionSearchApp(root)
    root.mainloop()
