import pandas as pd
from io import StringIO
from os import walk
from datetime import datetime


def float(data):
    return float(data.replace(',', '.'))


class Data:
    def __init__(self):
        self.data = []
        self.str_data = ""

    def read_from_dir(self, direct):
        for (_, _, filenames) in walk(direct):
            for file in filenames:
                self.str_read(direct + "\\" + file)

    def lines_read(self, file, skip=2):
        with open(file) as txt:
            lines = txt.readlines()[skip:]
            txt.close()
        return lines

    def str_read(self, file, skip=2, date=False, float_replace=False):
        lines = self.lines_read(file, skip)
        if float_replace:
            for i, word in enumerate(lines):
                if ',' in word:
                    lines[i] = word.replace(',', '.')
        if date:
            self.str_data += "".join(self.tab_datetime(lines))
        else:
            self.str_data += "".join(lines)

    def read(self, cols, index=None, sort_index=None, sep="\s+"):
        if index is None:
            index = []
        self.data = pd.read_csv(StringIO(self.str_data), sep=sep, index_col=index, names=cols)
        if not sort_index is None:
            self.data = self.data.sort_values(sort_index)

    @staticmethod
    def tab_datetime(lines):
        data = []
        for line in lines:
            words = line.split()

            words[1] += ";" + words[2]
            if len(words[1]) < 18:
                words[1] += ':00'
            words.pop(2)
            data.append("\t".join(words) + "\n")
        return data
