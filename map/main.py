# Import necessary packages
import os
import folium
from folium import plugins
import read_data

# import rasterio as rio
# from rasterio.warp import calculate_default_transform, reproject, Resampling

# Import data from EarthPy
folium_map = folium.Map(tiles="CartoDB dark_matter", location=[52.2167, 21.0],
                        zoom_start=2.5)

otdeli = [[55.716, 37.731, "Россия", "Центральное отделение компании ", "Москва, Люблинская ул., Д 5, КОРП 4",
           "Сафронова Евгения Анатольевна", 1000, 1],
          [59.939, 30.315, "Россия", "Филиал компании в Санкт-Петербурге", "Санкт-Петербург, Искровский пр., дом 22 А",
           "Яманаев Андрей Викторович", 250, 0],
          [56.316667, 44, "Россия", "Филиал компании в Нижнем Новгороде", "Нижний Новгород, пр. Ленина, 100",
           "Зиновьев Василий Валентинович", 400, 0],
          [40.923084, -73.839054, "США", "Американский филиал компании", "NY 10552, Mt Vernon, 33 William St",
           "Эбигейл Гибсон", 25, 1],
          [40, 40, "Китайский филиал компании", "Китай", "", "Тедань Хуан", 43, 0],
          [52.502044, 13.413828, "Германия", "Немецкий филиал компании", "10969 Berlin, Prinzessinnenstraße 29",
           "Алекс Гросс", 43, 1]]

for tip in otdeli:
    pop = ""
    for t in tip[2:7]:
        pop += str(t) + '\n'
    pop += "Функционирует" if tip[7] == 1 else "Не функционирует"
    marker = folium.Marker(location=[tip[0], tip[1]],
                           popup=pop,  # pop-up label for the marker
                           icon=folium.Icon())
    marker.add_to(folium_map)

dataset = read_data.Data()
lines = dataset.lines_read("E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\map\\GPSO.dat", 1)
gg = []
for i in range(0, len(lines) - 1, 1):
    setter = lines[i].split('\t')
    setter[1].replace(" ", ";")
    dataset.str_data += "\t".join(setter)
dataset.read(['name', "date", "transport", "la", "lo"], sep="\t")
print(dataset.data)
input()

dataset.str_read("E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\map\\Москва\\msk.dat", 1)
dataset.read(["La", "Lo", "E"], sep=',')
points = []
for la, lo, e in dataset.data.values:
    points.append([la, lo])
    # marker = folium.CircleMarker(location=[la, lo], radius=1)
    # marker.add_to(folium_map)

folium.PolyLine(points, color="blue", weight=2.5, opacity=1, popup="123").add_to(folium_map)
folium_map.save("my_map.html")
