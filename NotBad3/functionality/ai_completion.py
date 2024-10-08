from typing import Any
from keras.preprocessing.sequence import pad_sequences
import numpy as np


class AiCompletion:

    def __init__(self):
        self.data = []

        self.model_n_prev: dict[int, Any] = {1: None, 2: None}
        self.tokenizer = None
        self.encoded = None
        self.vocab_size = 0

        self.re = None
        self.is_pad_sequences_imported = False

        self.load_models_and_tokenizer()

    def is_valid_ver(self, n):

        return self.model_n_prev.get(n, None) is not None

    def _clean_text(self, text):
        words = text.split()
        clean_words = []

        for word in words:
            word = self.re.sub(r"\"| \?|—|-|\.|:|”|!|\*|;|,|“", ' ', word).strip()
            word = self.re.sub(r"’", "'", word).strip()
            word = word.lower()
            if word and (word.isalpha() or "'" in word) and (len(word) != 1 or word in ['i', 'a']):
                clean_words.append(word)

        return clean_words

    def _load_data_from_files(self):
        import os
        import re

        self.re = re

        print('-> loading new data...')

        parent_dir = './data'
        dir_data = os.listdir('./data')

        for dt_dir_data in dir_data:
            rootpath = parent_dir + '\\' + dt_dir_data
            txtFilesPaths = os.listdir(rootpath)

            for path in txtFilesPaths:
                if 'Copy' in path:
                    continue

                acc_path = rootpath + '\\' + path
                with open(acc_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                self.data.extend(self._clean_text(text))

        print('-> loading new data done.')

    def tokenize_and_encoded_new_data(self):

        from keras.preprocessing.text import Tokenizer
        from pickle import dump

        self._load_data_from_files()

        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts([self.data])
        self.vocab_size = len(self.tokenizer.index_word) + 1
        self.encoded = self.tokenizer.texts_to_sequences([self.data])[0]

        dump(self.tokenizer, open('../tokenizer.pkl', 'wb'))
        print('-> new Tokenizer saved.')

    def _make_train_seq_prev_words(self, n_perv_word=1):
        from keras.utils import to_categorical

        sequences = np.array([self.encoded[i - n_perv_word: i + 1]
                              for i in range(n_perv_word, len(self.encoded))])

        return sequences[:, :-1], \
            to_categorical(sequences[:, -1], num_classes=len(self.tokenizer.word_index) + 1), \
            n_perv_word + 1

    def _make_model(self, X, y, max_len: int, epos: int, callback=None):
        from keras.models import Sequential
        from keras.layers import Embedding, LSTM, Dense

        print('-> train model...')
        model = Sequential()
        model.add(Embedding(self.vocab_size, 10, input_length=max_len - 1))
        model.add(LSTM(50))
        model.add(Dense(self.vocab_size, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['accuracy'])

        if callback is None:
            model.fit(X, y, epochs=epos, verbose=2)
        else:
            model.fit(X, y, epochs=epos, verbose=2, callbacks=[callback])

        print('-> train model done.')

        return model

    def train_model(self, n_prev_words, new_data=False, epos=500, callback=None):

        if new_data:
            self.tokenize_and_encoded_new_data()

        X, y, max_len = self._make_train_seq_prev_words(n_prev_words)
        self.model_n_prev[n_prev_words] = self._make_model(X, y, max_len, epos, callback)
        self.model_n_prev[n_prev_words].save(f'models\\model_{n_prev_words}_prev.keras')

    def gen_top_next_word(self, model, seed_text, max_len, n_words):

        seq = np.array(self.tokenizer.texts_to_sequences([seed_text])[0])
        seq = pad_sequences([seq], maxlen=max_len - 1, padding='pre')

        yhat = model.predict_on_batch([seq])

        try:
            out_text = [self.tokenizer.index_word[i]
                        for i in np.argsort(yhat)[0][::-1][:n_words]]
        except KeyError:
            out_text = []

        return out_text

    def load_models_and_tokenizer(self):
        import os
        from keras.models import load_model
        from pickle import load

        print('-> loading models and tokenizer...')
        models_path = os.listdir('./models')
        for model_name in models_path:
            n = int(model_name.split("_")[1])
            self.model_n_prev[n] = load_model(f'models\\{model_name}')

        self.tokenizer = load(open('./tokenizer.pkl', 'rb'))
        print('-> loading models and tokenizer done')

    def predict(self, seed_text, model_nv=1, n_next_words=10):

        model = self.model_n_prev[model_nv]

        max_len = model_nv + 1
        result = self.gen_top_next_word(model, seed_text, max_len, n_next_words)
        return result
