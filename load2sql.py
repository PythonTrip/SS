import sqlite3
import critical_value as cv
import read_data
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from Plotter import *
import pandas as pd

cv.create_table()

direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\dataframes"
cols = ['num', 'date', "oC", 'vsu', 'W', 'congestion', 'Hours']
cr2cols = {
    "С": "oC",
    "ву/вс": 'vsu',
    "загрузка": 'congestion',
    "кВт": 'W',
    "часов": 'Hours'
}
index = ['date']
key = "oC"

dataset = read_data.Data()
dataset.read_from_dir(direct)
dataset.read(cols, index, ["num", "date"])

dataset.data.index = np.array([datetime.strptime(x, '%d.%m.%Y;%H:%M:%S') for x in dataset.data.index])

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cv.dataset.data.to_sql("critical", conn, if_exists="replace")

dataset.data.to_sql("telemetry", conn, if_exists="replace")
cursor.execute("""SELECT *
                    FROM telemetry"""
               )
dataset.data = pd.read_sql_query("select num, oC from telemetry ", conn)

print(dataset.data)
