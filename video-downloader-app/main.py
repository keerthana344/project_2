import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import yt_dlp
import threading


class VideoDownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        self.add_widget(Label(
            text="Video Downloader App",
            font_size=28,
            size_hint_y=None,
            height=60,
            bold=True
        ))

        self.url_input = TextInput(
            hint_text="Paste video URL here (e.g. YouTube link)...",
            size_hint_y=None,
            height=50,
            multiline=False,
            font_size=16
        )
        self.add_widget(self.url_input)

        self.status_label = Label(
            text="Ready to download...",
            size_hint_y=None,
            height=40,
            font_size=14
        )
        self.add_widget(self.status_label)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=25
        )
        self.add_widget(self.progress_bar)

        self.download_btn = Button(
            text="Download Video",
            size_hint_y=None,
            height=55,
            font_size=18,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Error: Please enter a valid URL."
            return

        self.status_label.text = "Downloading..."
        self.download_btn.disabled = True
        self.progress_bar.value = 0

        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = (downloaded / total) * 100
                Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', percent))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Downloading... {percent:.1f}%"))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 100))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Download Complete!"))

    def download_video(self, url):
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True,
            'noprogress': True,
            'progress_hooks': [self.progress_hook],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Download Complete!"))
        except Exception as e:
            error_msg = str(e)[:80]
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Failed: {error_msg}"))
        finally:
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))


class VideoDownloaderApp(App):
    def build(self):
        self.title = "Video Downloader"
        return VideoDownloaderLayout()


if __name__ == "__main__":
    VideoDownloaderApp().run()
