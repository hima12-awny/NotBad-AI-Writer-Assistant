from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy
from PySide6.QtCore import Qt, QTimer


# class LoadingDialog(QDialog):
#     def __init__(self, window_title: str, label_text: str):
#         super().__init__()
#         self.setWindowTitle(window_title)
#         self.setModal(True)
#         self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
#         layout = QVBoxLayout()
#         self.label = QLabel(label_text)
#         layout.addWidget(self.label)
#         self.setLayout(layout)


# class LoadingDialog(QDialog):
#     def __init__(self, window_title: str, label_text: str):
#         super().__init__()
#         self.setWindowTitle(window_title)
#         self.setModal(True)
#         self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
#
#         layout = QVBoxLayout()
#
#         self.label = QLabel(label_text)
#         layout.addWidget(self.label)
#
#         # Create an infinitely loading progress bar
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 0)  # Set the range to 0,0 to create an indeterminate progress bar
#         layout.addWidget(self.progress_bar)
#
#         self.setLayout(layout)
#
#         # Optional: Add a timer to update the progress bar's visual state
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_progress_bar)
#         self.timer.start(50)  # Update every 50 milliseconds
#
#     def update_progress_bar(self):
#         # This is just to keep the progress bar animated; it's not actually changing progress.
#         # The progress bar will appear as a continuously moving animation.
#         self.progress_bar.setValue((self.progress_bar.value() + 1) % 100)


class LoadingDialog(QDialog):
    def __init__(self, window_title: str, label_text: str):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        # Create layout
        layout = QVBoxLayout()

        # Create and add label
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)  # Center align the text
        self.label.setWordWrap(True)  # Enable text wrapping for better resizing
        layout.addWidget(self.label)

        # Create and add progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Set the range to 0, 0 to create an indeterminate progress bar
        self.progress_bar.setTextVisible(False)  # Hide the percentage text

        # Set size policy for progress bar
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Flexible width, fixed height
        layout.addWidget(self.progress_bar)

        # Apply layout to dialog
        self.setLayout(layout)

        # Optional: Add a timer to update the progress bar's visual state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(50)  # Update every 50 milliseconds

        # Adjust size policies and minimum sizes to ensure flexibility
        self.setMinimumSize(300, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_progress_bar(self):
        # This is just to keep the progress bar animated; it's not actually changing progress.
        self.progress_bar.setValue((self.progress_bar.value() + 1) % 100)

