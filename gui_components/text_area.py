from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QTextEdit, QLabel, QWidget, QApplication, QVBoxLayout
from gui_components.drop_shadow import DropShadow
import sys


class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        # Insert plain text from the source
        self.insertPlainText(source.text())


class TextArea(QWidget):
    def __init__(self,
                 parent=None,
                 border_radius=30,
                 blur_radius=30):
        """
        A custom QTextEdit with a footer that displays the word count and line count.

        :param parent: The parent widget.
        :param border_radius: The border radius of the QTextEdit.
        :param blur_radius: The blur radius of the drop shadow effect.
        """

        super().__init__(parent)

        # Create the QTextEdit
        self.text_edit = PlainTextEdit(self)
        self.text_edit.setGeometry(18, 30, 963, 655)  # Adjusted height to accommodate footer

        self.text_edit.setStyleSheet(
            '''
            QTextEdit{
             color: #000;
             border-top-left-radius: ''' + f'{border_radius}px; ' +
            'border-top-right-radius: ' + f'{border_radius}px; ' +
            'border-bottom-left-radius: 0px; ' +
            'border-bottom-right-radius: 0px; ' +
            '''background-clip: border;
               background-color: rgb(255, 255, 255);
               font: 18px;
               border: 4px solid;
               border-color: rgb(255, 255, 255);
               padding: 10px;
            }
            '''
        )
        self.text_edit.setAcceptRichText(False)
        self.text_edit.setFocus()
        self.text_edit.setPlaceholderText('write here')
        self.text_edit.setGraphicsEffect(DropShadow(self, blur_radius=blur_radius))

        # Create the footer QLabel
        self.footer = QLabel(self)
        self.footer.setStyleSheet(
            '''
            QLabel{
                font: 16px;
                color: #000;
                padding: 5px;
                font-weight: 600;
                background-color: #D3D3D3;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 10px; 
                border-bottom-right-radius: 10px; 
            }
        '''

        )

        self.footer.setText('Word count: 0 | Lines count: 0')

        # Layout
        layout_ = QVBoxLayout(self)
        layout_.addWidget(self.text_edit)
        layout_.addWidget(self.footer)
        layout_.setSpacing(0)
        layout_.setContentsMargins(5, 5, 5, 5)

        self.setLayout(layout_)

        # Connect the textChanged signal to update the word count
        self.text_edit.textChanged.connect(self.update_word_count)
        # self.show()

    def update_word_count(self):
        # Get the text from the QTextEdit
        text = self.text_edit.toPlainText()

        # Count words
        word_count = len([word.isalpha() for word in text.split()])

        line_count = text.count('\n') + 1

        # Update the footer
        self.footer.setText(f'Word count: {word_count} | Line count: {line_count}')

    def setText(self, text):
        self.text_edit.setText(text)

    def toPlainText(self):
        return self.text_edit.toPlainText()

    def cursorPositionChanged(self, callback):
        self.text_edit.cursorPositionChanged.connect(callback)

    def selectionChangedConnect(self, callback):
        self.text_edit.selectionChanged.connect(callback)

    def selectionChangedDisconnect(self, callback):
        self.text_edit.selectionChanged.disconnect(callback)

    def textCursor(self):
        return self.text_edit.textCursor()

    def cursorRect(self):
        return self.text_edit.cursorRect()

    def setFocus(self):
        self.text_edit.setFocus()

    def setContextMenuPolicy(self, policy):
        self.text_edit.setContextMenuPolicy(policy)

    def customContextMenuRequested(self, callback):
        self.text_edit.customContextMenuRequested.connect(callback)

    def clear(self):
        self.text_edit.clear()

    def insertPlainText(self, text):
        self.text_edit.insertPlainText(text)


# Example usage if needed
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout(window)

    text_area = TextArea(blur_radius=10)
    layout.addWidget(text_area)

    window.setLayout(layout)
    window.setGeometry(100, 100, 1000, 700)
    window.show()

    sys.exit(app.exec())
