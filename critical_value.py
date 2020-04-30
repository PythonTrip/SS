from read_data import Data

direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\crit\\crit.dat"
cols = ["GG", "Warning", "Type"]
index = False

dataset = Data()
cr2cols = {
    "С": "oC",
    "ву/вс": 'vsu',
    "загрузка": 'congestion',
    "кВт": 'W',
    "часов": 'Hours'
}


def get_value(key, param):
    mask = dataset.data['Type'] == param
    return float(dataset.data[mask][key].values[0])


def create_table():
    dataset.str_read(direct, 0)
    slices = dataset.str_data.split('\n')[1:]
    dataset.str_data = ""
    for i in slices:
        word = i.split("\t")[::-1]
        if len(word) > 1:
            if 'системы;%:00' in word:
                word[2] = 'загрузка'
            dataset.str_data += " ".join(word[:3]) + "\n"

    dataset.read(cols, index, ['Type'])

    dataset.data["Type"] = [cr2cols[x] for x in dataset.data["Type"]]


def check_param(param, value, percent=1):
    mask = dataset.data['Type'] == param
    data = dataset.data[mask]
    warning = data["Warning"].values
    gg = data["GG"].values
    if warning > value:
        return 0, float(warning - value)
    elif gg * percent > value:
        return 1, float(gg - value)
    elif gg >= value > gg * percent:
        return 2, float(gg - value)
    else:
        return 3, float(value - gg)


def warning(x, p):
    print(f"До опасного: {x} {p}")


def dangerous(x, p):
    print(f"До критического значения: {x} {p}")


def critical(x, p):
    print(f"ВНИМАНИЕ, ДО ПРЕВЫШЕНИЯ КРИТИЧЕСКОГО ЗНАЧЕНИЯ: {x} {p}")
    print(f"Вам необходимо {recommendation_critical[p]}")


def death(x, p):
    print(f"Оборудование сломано: предел {p} превышен на {x} ")
    print(f"Вам необходимо {recommendation_death[p]}")


err = {
    0: warning,
    1: dangerous,
    2: critical,
    3: death
}
recommendation_death = {
    "С": "выключить и охладить установку",
    "ву/вс": "охладить установку",
    "загрузка": "уменьшить нагрузку на установку",
    "кВт": "уменьшить нагрузку на установку",
    "часов": "остановить процесс и выключить оборудование",
}
recommendation_critical = {
    "С": "охладить установку",
    "ву/вс": "охладить установку",
    "загрузка": "уменьшить нагрузку на установку",
    "кВт": "уменьшить нагрузку на установку",
    "часов": "в скором времени потребуется отключить установку"
}
if __name__ == '__main__':
    create_table()
