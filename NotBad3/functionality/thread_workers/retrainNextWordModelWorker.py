from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from keras.callbacks import Callback


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
