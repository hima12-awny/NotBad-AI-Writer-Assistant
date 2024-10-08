from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from gui_components.set_n_prev_words import (
    set_n_prev_words,
    info_and_train_next_word_model
)


class WordAssistantMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Word Assistant")
        self.parent = parent

        self.add_next_word_ai()
        self.add_next_word_counter()
        self.add_word_completion()

    def add_next_word_ai(self):
        menu_next_word_ai = QMenu("Next Word With AI", self)

        self.parent.acs_next_word_ai = {
            "turn on":
                [
                    QAction('Turn On', menu_next_word_ai),
                    self.parent.switch_handler.switch_ai_next_word_prediction
                ],

            "num of words":
                [
                    QAction(f'Set Num of Prev Words ({self.parent.n_prev_word})', menu_next_word_ai),
                    lambda: set_n_prev_words(self.parent, True)
                ],

            "retrain model":
                [
                    QAction('Retrain Model', menu_next_word_ai),
                    lambda: info_and_train_next_word_model(self.parent)
                ]
        }

        for _, (action, callback) in self.parent.acs_next_word_ai.items():
            action.triggered.connect(callback)
            menu_next_word_ai.addAction(action)

        self.parent.acs_next_word_ai['num of words'][0].setEnabled(False)
        self.parent.acs_next_word_ai['retrain model'][0].setEnabled(False)

        self.addMenu(menu_next_word_ai)

    def add_next_word_counter(self):
        menu_next_word_counter = QMenu("Next Word With Counter", self)
        self.parent.acs_next_word_counter = {
            "turn on": [
                QAction('Turn On', self),
                self.parent.switch_handler.switch_counter_next_word_prediction
            ],

            "num of words":
                [
                    QAction(f'Set Num of Prev Words ({self.parent.n_prev_word})', self),
                    lambda x: set_n_prev_words(self.parent, False)
                ],
        }
        for _, (action, callback) in self.parent.acs_next_word_counter.items():
            action.triggered.connect(callback)
            menu_next_word_counter.addAction(action)

        self.parent.acs_next_word_counter['num of words'][0].setEnabled(False)
        self.addMenu(menu_next_word_counter)

    def add_word_completion(self):

        self.parent.action_word_completion = QAction("Word Completion (Turn Off)", self)
        self.parent.action_word_completion.triggered.connect(self.parent.switch_handler.switch_word_completion)
        self.addAction(self.parent.action_word_completion)
