from PySide6.QtWidgets import QMainWindow
from typing import Any
from functionality.ai_completion import AiCompletion
from functionality.next_word_with_counter import NextWordCounter
from functionality.threads_handler import load_next_word_ai_data


class SwitchingHandler:
    def __init__(self, parent: QMainWindow | Any):
        self.parent = parent

    def switch_ai_next_word_prediction(self):
        if self.parent.ai_next_word_is_on:
            self.parent.ai_next_word_is_on = 0
            self.parent.acs_next_word_ai['turn on'][0].setText('Turn on')
            self.parent.acs_next_word_ai['num of words'][0].setEnabled(0)
            self.parent.acs_next_word_ai['retrain model'][0].setEnabled(0)
            self.parent.sug_words_options.hide()

        else:
            if not self.parent.ai_tools_is_loaded:
                load_next_word_ai_data(self.parent)

            if self.parent.ai_tools_is_loaded:
                self.parent.ai_next_word_is_on = 1

            self.parent.acs_next_word_ai['turn on'][0].setText('Turn off')
            self.parent.acs_next_word_ai['num of words'][0].setEnabled(1)
            self.parent.acs_next_word_ai['retrain model'][0].setEnabled(1)

            if self.parent.counter_is_on:
                self.switch_counter_next_word_prediction()

            if self.parent.ai_tools_is_loaded:
                self.parent.ai_next_word_is_on = 1
                self.parent.word_tracker.track_sug_words()

    def switch_counter_next_word_prediction(self):

        if self.parent.counter_is_on:
            self.parent.counter_is_on = 0
            self.parent.acs_next_word_counter['turn on'][0].setText('Turn on')
            self.parent.acs_next_word_counter['num of words'][0].setEnabled(0)
        else:
            if not self.parent.counter_tools_is_loaded:
                self.parent.counter_next_word_prid = NextWordCounter()
                self.parent.counter_tools_is_loaded = 1

            self.parent.counter_is_on = 1
            self.parent.acs_next_word_counter['turn on'][0].setText('Turn Off')
            self.parent.acs_next_word_counter['num of words'][0].setEnabled(1)

            if self.parent.ai_next_word_is_on:
                self.switch_ai_next_word_prediction()

            self.parent.word_tracker.track_sug_words()

    def switch_word_completion(self):
        if self.parent.word_completion_is_on:
            self.parent.word_completion_is_on = 0
            self.parent.action_word_completion.setText('Word Completion (turn on)')
            self.parent.sug_words_options.hide()
        else:
            self.parent.word_completion_is_on = 1
            self.parent.action_word_completion.setText('Word Completion (turn off)')
            self.parent.word_tracker.track_sug_words()

