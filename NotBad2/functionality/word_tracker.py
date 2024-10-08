from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMainWindow
from typing import Any
from functionality.general import isSubString
from itertools import islice
from gui_components.set_n_prev_words import set_n_prev_words
from functools import lru_cache


class WordTracker:

    def __init__(self, parent: QMainWindow | Any):
        self.parent = parent
        self.tracked_words = None

    def get_n_prev_words(self):

        cursor_words = self.parent.txtArea.textCursor()
        cursor_words.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        if cursor_words.selectedText().strip().isalpha():
            cursor_words.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor)
            return False

        for i in range(self.parent.n_prev_word):
            cursor_words.movePosition(QTextCursor.MoveOperation.WordLeft, QTextCursor.MoveMode.KeepAnchor)

        self.tracked_words = cursor_words.selectedText()
        return True

    def track_with_next_word(self):

        if self.tracked_words and \
                not self.tracked_words[-1].isalpha():

            self.tracked_words = self.tracked_words.strip()

            if self.parent.ai_next_word_is_on:

                if not self.parent.ai_next_word_prid.is_valid_ver(self.parent.n_prev_word):
                    set_n_prev_words(self.parent, isForAi=True)
                    return False

                if self.parent.ai_next_word_prid.is_valid_ver(self.parent.n_prev_word):
                    self.parent.sug_word_list = self.parent.ai_next_word_prid.predict(
                        self.tracked_words, self.parent.n_prev_word, 50)

                return True

            elif self.parent.counter_is_on:
                self.parent.sug_word_list = (self.parent.counter_next_word_prid
                                             .get_next(self.tracked_words,
                                                       self.parent.txtArea.toPlainText()))
                return True

        return False

    @lru_cache(maxsize=10000)
    def get_sug_words(self, last_word):

        _sug_word_list = []
        counter = 0
        last_word_len = len(last_word)

        for i in range(last_word_len, 45 + 1):
            if i in self.parent.dict_of_all_sug_words:
                for word in self.parent.dict_of_all_sug_words[i]:
                    is_sub, n_matches = isSubString(last_word, word)
                    if is_sub:
                        _sug_word_list.append((n_matches, word))
                        counter += 1

                        if counter == 50:
                            break
            if counter == 50:
                break

        _sug_word_list.sort(key=lambda p: p[0], reverse=True)
        _sug_word_list.sort(key=lambda p: len(p[1]))
        _sug_word_list = [word[1] for word in _sug_word_list]
        return _sug_word_list

    def track_with_word_completion(self):

        if self.tracked_words and \
                self.tracked_words[-1].isalpha() and \
                self.parent.word_completion_is_on:
            last_word = self.tracked_words.split()[-1]

            self.parent.sug_word_list = self.get_sug_words(last_word)
            return True

        return False

    def track_sug_words(self):

        if self.get_n_prev_words() and (self.track_with_word_completion() or self.track_with_next_word()):
            self.parent.sug_words_options.update_tracker(self.parent)
        else:
            if self.parent.sug_words_options.isVisible():
                self.parent.sug_words_options.hide()
