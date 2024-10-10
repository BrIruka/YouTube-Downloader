import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import sys
import subprocess
from threading import Thread
import base64
import ctypes
import tempfile
import shutil

LANGUAGES = {
    "English": {
        "name": "YouTube Downloader",
        "entry_label": "Enter video link:",
        "download_button": "Download",
        "status_label": "Waiting for action...",
        "status_label1": "Downloading video and audio...",
        "status_label2": "Merging video and audio...",
        "status_label3": "Done! File saved as ",
        "status_label_error": "Please enter a video link.",
        "status_label_error2": "Error during download."
    },
    "Українська": {
        "name": "YouTube Завантажувач",
        "entry_label": "Введіть силку на відео:",
        "download_button": "Завантажити",
        "status_label": "Очікування дій...",
        "status_label1": "Завантаження відео та аудіо...",
        "status_label2": "З'єднання відео та аудіо...",
        "status_label3": "Завершено! Файл збережено як ",
        "status_label_error": "Будь ласка, введіть силку на відео.",
        "status_label_error2": "Помилка при завантаженні."
    },
    "Polski": {
        "name": "Pobieracz YouTube",
        "entry_label": "Wpisz link do wideo:",
        "download_button": "Pobierz",
        "status_label": "Oczekiwanie na działanie...",
        "status_label1": "Pobieranie wideo i audio...",
        "status_label2": "Łączenie wideo i audio...",
        "status_label3": "Gotowe! Plik zapisano jako ",
        "status_label_error": "Proszę podać link do wideo.",
        "status_label_error2": "Błąd podczas pobierania."
    },
    "Русский": {
        "name": "Загрузчик YouTube",
        "entry_label": "Введите ссылку на видео:",
        "download_button": "Загрузить",
        "status_label": "Ожидание действия...",
        "status_label1": "Загрузка видео и аудио...",
        "status_label2": "Объединение видео и аудио...",
        "status_label3": "Готово! Файл сохранен как ",
        "status_label_error": "Пожалуйста, введите ссылку на видео.",
        "status_label_error2": "Ошибка при загрузке."
    },
    "中文": {
        "name": "YouTube 下载器",
        "entry_label": "请输入视频链接：",
        "download_button": "下载",
        "status_label": "等待操作...",
        "status_label1": "正在下载视频和音频...",
        "status_label2": "正在合并视频和音频...",
        "status_label3": "完成！文件已保存为 ",
        "status_label_error": "请输入视频链接。",
        "status_label_error2": "下载过程中出错。"
    }
}


# Функція для завантаження відео та аудіо
def download_video_audio(video_link):
    ydl_opts_video = {
        'format': 'bestvideo',
        'outtmpl': '%(title)s_video.%(ext)s',  # Назва файлу відео
    }
    
    ydl_opts_audio = {
        'format': 'bestaudio',
        'outtmpl': '%(title)s_audio.%(ext)s',  # Назва файлу аудіо
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        info_dict_video = ydl.extract_info(video_link, download=True)
        video_file_path = ydl.prepare_filename(info_dict_video)
    
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        info_dict_audio = ydl.extract_info(video_link, download=True)
        audio_file_path = ydl.prepare_filename(info_dict_audio)
    
    return video_file_path, audio_file_path, info_dict_video['title']  # Повертаємо назву відео


def get_ffmpeg_path():
    # Якщо запускається з PyInstaller, ffmpeg буде вбудований у тимчасову директорію
    if getattr(sys, 'frozen', False):
        # PyInstaller виконує програму, зберігаючи ресурси в sys._MEIPASS
        return os.path.join(sys._MEIPASS, 'ffmpeg.exe')
    else:
        # Якщо запускається без PyInstaller, використовуємо локальний ffmpeg
        return os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

def merge_video_audio(video_file, audio_file, output_file):
    ffmpeg_path = get_ffmpeg_path()

    command = [
        ffmpeg_path, '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ]
    subprocess.run(command, check=True)



def create_icon_folder():
    icon_folder_path = os.path.expanduser("~/Documents/YouTubeDownloader_ico")
    os.makedirs(icon_folder_path, exist_ok=True)

    icon_path = os.path.join(icon_folder_path, "icon.ico")

    # Введіть ваш Base64 рядок тут
    icon_base64_here = "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"

    # Декодування Base64 рядка у байтовий формат
    icon_data = base64.b64decode(icon_base64_here)

    with open(icon_path, "wb") as icon_file:
        icon_file.write(icon_data)

    return icon_path

# Створення вікна з tkinter
class YouTubeDownloader:
    def __init__(self, master, language="English"):
        self.master = master
        master.title("YouTube Downloader")
        master.configure(bg="#2b2b2b")
        score_program = "500x220"
    # Мова
        button_frame = tk.Frame(master, bg="#2b2b2b")
        button_frame.pack(pady=(0, 2), padx=(0, 0),)
    
        self.language = language
        self.texts = LANGUAGES.get(language, LANGUAGES["English"])

        # Додайте кнопку LANG
        self.lang_button = tk.Button(button_frame, text="LANG", command=self.show_language_menu,
                                    bg="#444444", fg="red", relief=tk.FLAT,
                                    highlightcolor="red", highlightbackground="red", highlightthickness=2)
        self.lang_button.pack(side=tk.LEFT, padx=(0, 0), pady=(0, 0))

        self.language_var = tk.StringVar()
        self.language_var.set(language)

    #Author
        self.author_button = tk.Button(button_frame, text="AUTHOR", command=self.show_author_info,
                                   bg="#444444", fg="red", relief=tk.FLAT,
                                   highlightcolor="red", highlightbackground="red", highlightthickness=2)
        self.author_button.pack(side=tk.LEFT, padx=(0, 0), pady=(0, 0))

    ####
        # Отримання DPI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
        # Отримання розмірів монітора
        monitor_width = master.winfo_screenwidth()
        monitor_height = master.winfo_screenheight()
        # Визначення варіанту масштабування
        scale_factor = 1.0  # 1.0 - 100%
        if dpi == 120:
            scale_factor = 1.05  # 125%
        elif dpi == 144:
            scale_factor = 1.08   # 150%
        elif dpi == 168:
            scale_factor = 1.12  # 175%
        elif dpi == 192:
            scale_factor = 1.14  # 200%
        # Встановлення розмірів вікна Tkinter з урахуванням DPI та варіанту масштабування
        window_width = min(monitor_width, int(500 * scale_factor))
        window_height = min(monitor_height, int(220 * scale_factor))
        score_program = f"{window_width}x{window_height}"
        master.geometry(score_program)
        master.resizable(0, 0)
        
        # Заголовок
        self.title_label = tk.Label(master, text=self.texts["name"], font=("Arial", 16), fg="white", bg="#2b2b2b")
        self.title_label.pack(pady=10)
        
        # Поле для введення URL
        self.entry_label = tk.Label(master, text=self.texts["entry_label"], fg="white", bg="#2b2b2b")
        self.entry_label.pack(pady=5)
        
        global entry
        self.entry = tk.Text(master, width=40, height=1, state='normal')
        self.entry.pack(pady=5)
        
        # Кнопка для завантаження
        self.download_button = tk.Button(master, text=self.texts["download_button"], command=lambda: Thread(target=self.start_download).start(), bg="#3c3c3c", fg="white")
        self.download_button.pack(pady=10)
        
        # Статус
        global status_label
        self.status_label = tk.Label(master, text=self.texts["status_label"], fg="lightgreen", bg="#2b2b2b")
        self.status_label.pack(pady=5)
        

        # Отримання шляху до іконки або створення папки та іконки, якщо її ще немає
        icon_path = create_icon_folder()

        # Встановлення значка в вікні програми за допомогою ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(str(icon_path))
        master.iconbitmap(icon_path)

    def show_language_menu(self):
        # Створіть меню для вибору мови
        lang_menu = tk.Menu(self.master, tearoff=0, bg="#222222", fg="red")
        for lang_code, lang_name in LANGUAGES.items():
            lang_menu.add_command(label=lang_code, command=lambda lang=lang_code: self.on_language_change(lang))
    
        # Покажіть меню після кнопки LANG
        lang_menu.post(self.lang_button.winfo_rootx(), self.lang_button.winfo_rooty() + self.lang_button.winfo_height())

    def set_language(self, language):
            if language in LANGUAGES:
                self.language = language
                self.texts = LANGUAGES[language]

    def on_language_change(self, language):
        self.set_language(language)
        self.update_texts()

    def update_texts(self):
        self.title_label.config(text=self.texts["name"])
        self.entry_label.config(text=self.texts["entry_label"])
        self.download_button.config(text=self.texts["download_button"])
        self.status_label.config(text=self.texts["status_label"])
        # Оновіть тексти для інших інтерфейсних елементів тут 

    # Основна функція завантаження та з'єднання
    def start_download(self):
        video_link = self.entry.get("1.0", tk.END).strip()  # отримаємо весь текст з Text віджету

        if not video_link:
            self.status_label.config(text=self.texts["status_label_error"])
            return
        
        try:
            self.status_label.config(text=self.texts["status_label1"])
            video_file, audio_file, video_title = download_video_audio(video_link)
            
            self.status_label.config(text=self.texts["status_label2"])
            output_file = f"{video_title}.mp4"  # Кінцевий файл з назвою відео
            merge_video_audio(video_file, audio_file, output_file)
            
            self.status_label.config(text=f"{self.texts['status_label3']} {output_file}")

            # Видалення проміжних файлів
            os.remove(video_file)
            os.remove(audio_file)
            
        except Exception as e:
            self.status_label.config(text=self.texts["status_label_error2"], fg="red", bg="#2b2b2b")

    def show_author_info(self):
        self.show_author_menu()

    def show_author_menu(self):
        author_menu = tk.Menu(self.master, tearoff=0, bg="#222222", fg="red")
        links = {
            'GitHub': "https://github.com/BrIruka"
            # Додайте інші посилання тут, якщо потрібно
        }
        
        for label_text, url in links.items():
            author_menu.add_command(label=label_text, command=lambda link=url: self.open_url(link))
        
        author_menu.post(self.author_button.winfo_rootx(), self.author_button.winfo_rooty() + self.author_button.winfo_height())

    
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

root = tk.Tk()
gui = YouTubeDownloader(root)

root.mainloop()
