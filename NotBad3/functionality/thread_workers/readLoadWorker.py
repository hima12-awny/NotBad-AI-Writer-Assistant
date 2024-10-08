from PySide6.QtCore import QObject, Signal


class ReadLoadWorker(QObject):
    finished = Signal()

    def __init__(self, text, audio_file='temp_audio.mp3'):
        super().__init__()
        self.text = text
        self.audio_file = audio_file
        self._is_running = True

        import threading
        self._stop_event = threading.Event()

    def run(self):
        import pygame
        from gtts import gTTS
        import os
        from functionality.file_handlling import read_attr_from_settings

        self._is_running = True
        try:
            read_lang_code = read_attr_from_settings("read_lang_code")
            tts = gTTS(text=self.text, lang=read_lang_code)
            tts.save(self.audio_file)

            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if not self._is_running:
                    pygame.mixer.music.stop()
                    break
                pygame.time.wait(100)

        finally:
            pygame.mixer.quit()
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)

        self.finished.emit()

    def stop(self):
        self._is_running = False
        self._stop_event.set()
        self.finished.emit()
