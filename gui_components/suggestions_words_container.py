from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QListWidget, QMainWindow
from gui_components.drop_shadow import DropShadow
from typing import Any


class SuggestionsWordsContainer(QListWidget):

    def __init__(self, parent: QMainWindow):

        super().__init__(parent)

        self.setGeometry(0, 0, 200, 200)
        self.setStyleSheet('''
                QListWidget{ 
                        border-radius: 10px;
                        background-clip: border;
                        background-color: rgb(255, 255,255);
                        font: 16px;
                        border:4px solid;
                        border-color: rgb(255,255,255);
                        padding:10px;
                    }''')

        self.setWordWrap(True)
        self.setGraphicsEffect(DropShadow(self, 10))
        self.activated.connect(lambda: self.add_suggested_word(parent, False))
        self.hide()

    def add_suggested_word(self,
                           parent: QMainWindow | Any,
                           set_first_word: int):

        if parent.sug_word_list and not self.isHidden():

            cursorWord = parent.txtArea.textCursor()
            cursorWord.movePosition(QTextCursor.MoveOperation.WordLeft, QTextCursor.MoveMode.KeepAnchor)
            in_word = cursorWord.selectedText()

            # all_txt = parent.txtArea.toPlainText()
            # put_space = (all_txt.rfind(in_word) + len(in_word)) == len(all_txt)

            text = parent.sug_words_options.itemAt(0, 0).text() if set_first_word \
                else self.currentItem().text()

            if len(in_word) > 1 and in_word[-1] == ' ':
                text = in_word + text

            # text += ' ' if put_space else ''

            text += ' '

            cursorWord.insertText(text)
            parent.txtArea.setFocus()

    def update_tracker(self, parent: QMainWindow | Any):

        self.resize(200, 200)
        curser_position = parent.txtArea.cursorRect()
        self.clear()

        self.addItems(parent.sug_word_list)

        self.move(curser_position.x() + 38, curser_position.y() + 45)
        self.show()

    def switch_focus(self, parent: QMainWindow | Any):
        if self.hasFocus():
            parent.txtArea.setFocus()
        else:
            self.setFocus()
            self.setCurrentRow(0)
