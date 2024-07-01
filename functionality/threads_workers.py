import pygame
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from keras.callbacks import Callback
from PySide6.QtWidgets import QMainWindow
from typing import Any
import threading
from gtts import gTTS
import os
from functionality.file_handlling import read_attr_from_settings
from gui_components.set_ai_api_key import ApiKeyInputDialog


class RetrainNextWordModelWorker(QObject, Callback):
    def __init__(self,
                 ai_next_word_model,
                 n_prv_words,
                 n_epochs):
        super().__init__()
        self.ai_next_word_model = ai_next_word_model
        self.n_prv_words = n_prv_words
        self.n_epochs = n_epochs

    finished = Signal()
    progress = Signal(int)

    def on_epoch_end(self, epoch, logs=None):
        self.progress.emit(1)

    def run(self):
        self.ai_next_word_model.train_model(
            self.n_prv_words,
            new_data=1,
            epos=self.n_epochs,
            callback=self
        )

        self.finished.emit()


class ReadLoadWorker(QObject):
    finished = Signal()

    def __init__(self, text, audio_file='temp_audio.mp3'):
        super().__init__()
        self.text = text
        self.audio_file = audio_file
        self._is_running = True
        self._stop_event = threading.Event()

    def run(self):
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


class AITaskWorker(QObject):
    finished = Signal()  # Signal to indicate completion with a message

    def __init__(self, func, parent_window: QMainWindow | Any):
        super().__init__()
        self.func = func
        self.parent_window = parent_window

    def run(self):

        try:
            self.parent_window.output_result_text = self.func()

        except Exception as e:
            error_text = ','.join(e.args)

            if error_text in [
                '[Errno 11001] getaddrinfo failed',
                'Connection error.'
            ]:
                error_text = 'ERROR: Internet Connection error. Check your Network Connection and Try Agin.'

            if 'Error code: 401' in error_text:
                error_text = 'ERROR: Check your API Key and Try Again.'

            self.parent_window.output_result_text = error_text

        self.finished.emit()
