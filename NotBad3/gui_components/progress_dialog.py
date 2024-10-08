from PySide6.QtWidgets import QDialog


class ProgressDialog(QDialog):
    def __init__(self,
                 max_steps,
                 n_prev_words,
                 window_title,
                 label_title,
                 finsh_text):

        self.finsh_text = finsh_text
        self.window_title = window_title
        self.label_title = label_title

        super().__init__()
        self.max_step = max_steps
        self.n_prev_words = n_prev_words
        self.progressBar = None
        self.lblTxt = None
        self.value = 0

        self.initUI()

    def initUI(self):
        from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout

        self.lblTxt = QLabel(self)
        self.lblTxt.setText(self.label_title)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(0, 0, 300, 25)
        self.progressBar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self.lblTxt)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

        # self.setWindowTitle('Training Model')
        self.setWindowTitle(self.window_title)
        self.show()

    def updateProgress(self):
        self.value += 1
        percent = round((self.value / self.max_step) * 100)
        self.progressBar.setValue(percent)
        if self.value == self.max_step:

            # self.lblTxt.setText('Done, you have train a new '
            #                     f'model with {self.n_prev_words} of Previous words\nNOTE: Now you use version of '
            #                     f'{self.n_prev_words} prev words')

            self.lblTxt.setText(self.finsh_text)
