import critical_value as cv
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from Plotter import *
from math import ceil

cv.create_table()

conn = sqlite3.connect("mydatabase.db")  #
cursor = conn.cursor()


def create_telemetry_mask(crkey, crparam, k1, k2=None):
    if not k2 is None:
        arr = [f"{crkey} > {cv.get_value(crparam, crkey) * k1} AND "
               f"{crkey} < {cv.get_value(crparam, crkey) * k2}", 2, crkey]
        mask = arr[0]
        code = arr[1]
        key = arr[2]
    else:
        arr = [f"{crkey} > {cv.get_value(crparam, crkey) * k1}", 3, crkey]
        mask = arr[0]
        code = arr[1]
        key = arr[2]
    return [mask, code, key]


def create_date_mask(date1, date2):
    mask = f"datetime(date) >'{date1}' AND datetime(date) < '{date2}'"
    return mask


def update_plot(date1, date2):
    interval = (date2 - date1).days / 10
    if interval == 0:
        interval = (date2 - date1).seconds / (3600 * 12)
        date_limit([date1, date2], days=0, hours=2)
        _format = "%H"
        update_hour_formatter(format=_format, interval=ceil(interval))
    else:
        _format = "%d.%m %H"
        date_limit([date1, date2])
        update_day_formatter(format=_format, interval=ceil(interval))


def sum_mask(masks):
    out = "WHERE "
    for mask in masks:
        out += mask + " AND "
    return out[:len(out) - 5]


masks = [
    create_telemetry_mask('oC', 'GG', 0.95, 1),
    create_telemetry_mask('oC', 'GG', 1),

    create_telemetry_mask('vsu', 'GG', 0.95, 1),
    create_telemetry_mask('vsu', 'GG', 1),

    create_telemetry_mask('congestion', 'GG', 0.8, 0.95),
    create_telemetry_mask('congestion', 'GG', 0.95),

    create_telemetry_mask('W', 'GG', 0.95, 1),
    create_telemetry_mask('W', 'GG', 1),

    create_telemetry_mask('Hours', 'GG', 0.85, 1),
    create_telemetry_mask('Hours', 'GG', 1)
]
fig, ax = plt.subplots(1, sharex=True, sharey=False)
# ax.set_facecolor('seashell')
fig.set_facecolor('floralwhite')
plt.grid()
date1 = datetime(2020, 3, 1, 11)
date2 = datetime(2020, 3, 10, 11)

date_mask = create_date_mask(date1, date2)
num_mask = "num == 10"
final_mask = sum_mask([date_mask, num_mask, masks[1][0]])

print(f"WHERE datetime(date) >'{date1}' AND datetime(date) < '{date2}'")
new_data = pd.read_sql_query(f"select * from telemetry "
                             f"{final_mask}", conn, index_col="index")
update_plot(date1, date2)
y_limit([min(new_data["oC"]), max(new_data["oC"])], new_data["oC"].std())
plt.scatter(new_data['date'], new_data["oC"])
plt.show()
