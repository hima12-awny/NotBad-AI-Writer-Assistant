from typing import Any

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMainWindow


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
