import requests
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6 import uic


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/yaxzo_maps.ui", self)
        self.search_button.clicked.connect(self.get_coordinates)

    def set_map(self):
        if self.map_file != "No maps":
            self.pixmap = QPixmap(self.map_file)
            self.image = self.map_label
            self.image.resize(420, 540)
            self.image.setPixmap(self.pixmap)
        else:
            self.map_label.setText("По данному запросу ничего не найдено")

    def get_map_image(self, coordinates):
        STATIC_API_LINK = "https://static-maps.yandex.ru/1.x/?"

        address_ll = ",".join(coordinates.split())

        static_api_params = {
            "z": 14,
            "ll": address_ll,
            "l": "map"
        }

        response = requests.get(STATIC_API_LINK, params=static_api_params)

        if response:
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            file.close()
        else:
            self.map_file = "No maps"
        self.set_map()

    def get_coordinates(self):
        GEOCODER_API_LINK = "http://geocode-maps.yandex.ru/1.x/?"

        place = self.search_query.text()

        geo_params = {
            "apikey": # свой апи ключ геокодера,
            "geocode": place,
            "format": "json"
        }

        response = requests.get(GEOCODER_API_LINK, params=geo_params)

        if response:
            response_json = response.json()
            coordinate = \
                response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

            self.get_map_image(coordinate)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = MapWindow()
    map.show()
    sys.exit(app.exec())
