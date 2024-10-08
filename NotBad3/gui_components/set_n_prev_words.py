from PySide6.QtWidgets import QMainWindow, QInputDialog, QMessageBox
from typing import Any


def info_and_train_next_word_model(self, n_prev_words=None, n_epochs=200):
    if not n_prev_words:
        n_prev_words = self.n_prev_word

    ok = QMessageBox.information(self,
                                 'NOTE',
                                 "ok wait this take few minutes that is relay on "
                                 "(how big your data, number of epochs)\nNOTE: AI Completion "
                                 "will turned off while training")
    if not ok:
        return

    self.sug_words_options.hide()

    from functionality.threads_handler import make_thread_for_train_model
    make_thread_for_train_model(self, n_prev_words, n_epochs)


def set_n_prev_words(self: QMainWindow | Any, isForAi=True):
    n_prev_words, ok = QInputDialog.getInt(
        self,
        'Enter Number',
        'Enter Number of Previous Words',
        1, 1, 50
    )

    if not ok:
        return

    from functionality.file_handlling import write_attr_to_settings
    from functionality.threads_handler import update_n_prev_words

    write_attr_to_settings("n_prev_words", n_prev_words)

    if not isForAi:
        update_n_prev_words(self, n_prev_words, False)
        self.sug_words_options.update_tracker(self)
        return

    if self.ai_next_word_prid.is_valid_ver(n_prev_words):
        update_n_prev_words(self, n_prev_words, True)
        return

    reply = QMessageBox.question(self, 'NOTE',
                                 f'There is no Trained Model that can predict word that requiters {n_prev_words}'
                                 f' of'
                                 f' Previous words, so you want to train a new one to fit in your need?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.No:
        return

    n_epochs, ok = QInputDialog.getInt(self,
                                       'Enter Number',
                                       'Enter Number of epochs',
                                       20, 20, 1000)

    if not ok:
        return

    info_and_train_next_word_model(self, n_prev_words, n_epochs)
