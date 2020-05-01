import sqlite3
import read_data
import numpy as np
from datetime import datetime

dataset = read_data.Data()
lines = dataset.lines_read("E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\map\\GPSO.dat", 1)
gg = []
for i in range(0, len(lines) - 1, 1):
    setter = lines[i].split('\t')
    dataset.str_data += "\t".join(setter)
dataset.read(['name', "date", "transport", "la", "lo"], sep="\t")
dataset.data['date'][6] = dataset.data['date'][6][1:]
dataset.data['date'] = np.array([datetime.strptime(x, '%d.%m.%Y %H:%M') for x in dataset.data['date'].values])

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

dataset.data.to_sql("GPS", conn, if_exists="replace")


print(dataset.data)
