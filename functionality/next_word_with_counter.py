import re
import collections
import os
import textract


class NextWordCounter:
    def __init__(self):
        self.data = ''
        self.results = []
        self.read_data()

    def read_data(self):
        print()
        print('-> loading your data...')

        parent_dir = './data'
        dir_data = os.listdir('./data')

        for dt_dir_data in dir_data:
            rootpath = parent_dir + '\\' + dt_dir_data
            txtFilesPaths = os.listdir(rootpath)

            for path in txtFilesPaths:
                if 'Copy' in path:
                    continue

                text = textract.process(rootpath + '\\' + path).decode('utf-8')
                self.data += text.lower()

        print('-> loading your data done.')
        print()

    def get_next(self, text, currText):
        self.results.clear()
        self._get_next_local(text, currText)
        self._get_next_local(text, self.data)
        return self.results

    def _get_next_local(self, text, data):
        pattern = f"{text.lower()} \\w+"
        results = re.findall(pattern, data, re.IGNORECASE)
        results = collections.Counter(results).most_common(50)
        self.results.extend([word[0].split(' ')[-1] for word in results if word not in self.results])
