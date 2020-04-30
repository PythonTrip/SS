import read_data
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARMA
import statsmodels.api as sm
import numpy as np


def run_sequence_plot(x, y, title, xlabel="time", ylabel="series"):
    plt.plot(x, y, 'k-', label="actual")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(alpha=0.3)
    plt.legend()


direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\dataframes"
cols = ['#', 'date', "oC", 'vsu', 'W', '%', 'Hours']
index = ['date']
key = "oC"

dataset = read_data.Data()
dataset.read_from_dir(direct)
dataset.read(cols, index, ["#", "date"])

mask = dataset.data["#"] == 1
masked_data = dataset.data[mask]
print(masked_data.sample(frac=0.8, random_state=0))
