from PySide6.QtCore import QThread
from PySide6.QtCore import Signal

from functionality.threads_workers import RetrainNextWordModelWorker, ReadLoadWorker, AITaskWorker
from functionality.ai_completion import AiCompletion

from gui_components.loading_dialog import LoadingDialog
from gui_components.progress_dialog import ProgressDialog


class ReadAiNextWordModelData(QThread):

    def __init__(self, parent):
        super().__init__()  # Initialize the QThread base class

        self.parent = parent

    task_finished = Signal()

    def run(self):
        self.parent.ai_next_word_prid = AiCompletion()
        self.task_finished.emit()


def on_load_next_word_finish(self):
    self.loading_window.close()
    self.ai_next_word_is_on = 1
    self.ai_tools_is_loaded = 1
    self.word_tracker.track_sug_words()


def load_next_word_ai_data(self):
    self.loading_window = LoadingDialog(window_title='loading', label_text='loading next word model data...')
    self.loading_window.show()

    self.loading_next_word_data_thread = ReadAiNextWordModelData(self)
    self.loading_next_word_data_thread.task_finished.connect(lambda: on_load_next_word_finish(self))
    self.loading_next_word_data_thread.start()


def update_n_prev_words(self, n_prev_words, isForAi=True):
    self.n_prev_word = n_prev_words

    if isForAi:
        self.ai_next_word_is_on = 1
    self.acs_next_word_ai['num of words'][0].setText(f'Set Num of Prev Words ({self.n_prev_word})')
    # self.acs_next_word_counter['num of words'][0].setText(f'Set Num of Prev Words ({self.n_prev_word})')

    self.word_tracker.track_sug_words()


def make_thread_for_train_model(self, n_prev_words, epoch_num):
    self.ai_is_on = 0

    self.thread = QThread()

    self.worker = RetrainNextWordModelWorker(self.ai_next_word_prid, n_prev_words, epoch_num)

    self.progressbar = ProgressDialog(
        epoch_num,
        n_prev_words,
        label_title='Training the Model Loading:',
        window_title='Training Model',
        finsh_text='Done, you have train a new '
                   f'model with {n_prev_words} of Previous words\nNOTE: Now you use version of '
                   f'{epoch_num} prev words'
    )

    self.worker.moveToThread(self.thread)

    self.thread.started.connect(self.worker.run)
    self.thread.started.connect(self.progressbar.exec)

    self.worker.progress.connect(lambda: self.progressbar.updateProgress())
    self.worker.finished.connect(lambda: update_n_prev_words(self, n_prev_words, isForAi=True))

    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()


def read_load_mode_on(self):
    self.is_read_load_on = 1
    self.action_read_load.setText("Stop Reading")


def read_load_mode_off(self):
    self.is_read_load_on = 0
    self.action_read_load.setText("Start Read")


def make_thread_for_read_mode(self, text):
    self.thread = QThread()
    self.worker = ReadLoadWorker(text)
    self.worker.moveToThread(self.thread)

    self.thread.started.connect(lambda: read_load_mode_on(self))
    self.thread.started.connect(self.worker.run)
    self.worker.finished.connect(lambda: read_load_mode_off(self))

    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()


def stop_reading(self):

    if self.worker and self.thread and self.thread.isRunning():
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        self.worker = None
        self.thread = None


def on_ai_task_start(self):
    self.ai_task_is_running = True
    self.out_txtArea.setText(f"{self.function_name.title()} Loading...")
    self.controls_section.generate_button.disable_button()
    self.controls_section.insert_button.disable_button()


def on_ai_task_finish(self):
    self.ai_task_is_running = False
    self.out_txtArea.setText(self.output_result_text)
    self.controls_section.generate_button.enable_button()
    self.controls_section.insert_button.enable_button()


def make_thread_for_ai_task(self, func):
    self.ai_task_thread = QThread()
    self.ai_task_worker = AITaskWorker(
        func=func,
        parent_window=self
    )
    self.ai_task_worker.moveToThread(self.ai_task_thread)
    self.ai_task_thread.started.connect(lambda: on_ai_task_start(self))
    self.ai_task_thread.started.connect(self.ai_task_worker.run)
    self.ai_task_worker.finished.connect(lambda: on_ai_task_finish(self))

    self.ai_task_worker.finished.connect(self.ai_task_thread.quit)
    self.ai_task_worker.finished.connect(self.ai_task_worker.deleteLater)
    self.ai_task_thread.finished.connect(self.ai_task_thread.deleteLater)
    self.ai_task_thread.start()
