import critical_value as cv
import read_data
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from Plotter import *
from math import ceil

cv.create_table()

direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\dataframes"
cols = ['#', 'date', "oC", 'vsu', 'W', '%', 'Hours']
cr2cols = {
    "С": "oC",
    "ву/вс": 'vsu',
    "загрузка": '%',
    "кВт": 'W',
    "часов": 'Hours'
}
index = ['date']
key = "oC"

dataset = read_data.Data()
dataset.read_from_dir(direct)
dataset.read(cols, index, ["#", "date"])


class Telemetry:
    def __init__(self, data):
        self.data = data
        self.dates = self.index2datetime()

    def create_telemetry_mask(self, crkey, crparam, k1, k2=None):
        if not k2 is None:
            arr = [self.data[cr2cols[crkey]] >
                   cv.get_value(crparam, crkey) * k1,
                   self.data[cr2cols[crkey]] < cv.get_value(crparam, crkey) * k2, 2, crkey]
            mask = arr[0] & arr[1]
            code = arr[2]
            key = arr[3]
        else:
            arr = [self.data[cr2cols[crkey]] > cv.get_value(crparam, crkey), 3, crkey]
            mask = arr[0]
            code = arr[1]
            key = arr[2]
        return [mask, code, key]

    def create_date_mask(self, date1, date2):
        mask = (self.dates > date1) & (self.dates < date2)
        return mask

    def index2datetime(self):
        return np.array([datetime.strptime(x, '%d.%m.%Y;%H:%M:%S') for x in self.data.index])

    @staticmethod
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


telemetry = Telemetry(dataset.data)
masks = [
    telemetry.create_telemetry_mask('С', 'GG', 0.95, 1),
    telemetry.create_telemetry_mask('С', 'GG', 1),

    telemetry.create_telemetry_mask('ву/вс', 'GG', 0.95, 1),
    telemetry.create_telemetry_mask('ву/вс', 'GG', 1),

    telemetry.create_telemetry_mask('загрузка', 'GG', 0.8, 0.95),
    telemetry.create_telemetry_mask('загрузка', 'GG', 0.95),

    telemetry.create_telemetry_mask('кВт', 'GG', 0.95, 1),
    telemetry.create_telemetry_mask('кВт', 'GG', 1),

    telemetry.create_telemetry_mask('часов', 'GG', 0.85, 1),
    telemetry.create_telemetry_mask('часов', 'GG', 1)
]
fig, ax = plt.subplots(1, sharex=True, sharey=False)
# ax.set_facecolor('seashell')
fig.set_facecolor('floralwhite')
plt.grid()
date1 = datetime(2020, 3, 1, 0, 0, 0)
date2 = datetime(2020, 3, 30, 11, 0, 0)

date_mask = telemetry.create_date_mask(date1, date2)
num_mask = dataset.data["#"] == 10
final_mask = date_mask & num_mask & masks[1][0]
new_data = telemetry.data[final_mask]
telemetry.update_plot(date1, date2)
y_limit([min(new_data["oC"]), max(new_data["oC"])], new_data["oC"].std())
plt.scatter(telemetry.dates[final_mask], new_data["oC"])
plt.show()
