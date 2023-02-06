import requests
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from ui.yaxzo_maps import Ui_MainWindow


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.search_button.clicked.connect(self.get_coordinates)

        self.GEOCODER_API_LINK = "http://geocode-maps.yandex.ru/1.x/?"
        self.STATIC_API_LINK = "https://static-maps.yandex.ru/1.x/?"

        self.image = self.ui.map_label

        self.static_api_params = {
            "scale": 1.9,
            "z": 14,
            "l": "map"
        }

        self.geo_params = {
            "apikey": # свой апи ключ геокодера,
            "format": "json"
        }

    def set_map(self):
        if self.map_file != "No maps":
            self.pixmap = QPixmap(self.map_file)
            self.image = self.ui.map_label
            self.image.resize(600, 450)
            self.image.setPixmap(self.pixmap)
        else:
            self.ui.map_label.setText("По данному запросу ничего не найдено")

    def get_map_image(self, coordinates):
        address_ll = ",".join(coordinates.split())

        self.static_api_params["ll"] = address_ll

        response = requests.get(self.STATIC_API_LINK, params=self.static_api_params)

        if response:
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            file.close()
        self.set_map()

    def get_coordinates(self):
        place = self.ui.search_query.text()

        self.geo_params["geocode"] = place

        try:
            response = requests.get(self.GEOCODER_API_LINK, params=self.geo_params)

            if response:
                response_json = response.json()
                coordinate = \
                    response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

                self.get_map_image(coordinate)
            else:
                raise BaseException
        except BaseException:
            self.ui.map_label.setText("Место не найдено")
            self.image.setText("Место не найдено")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.image.text() != "Место не найдено":
                if self.static_api_params["scale"] < 4:
                    self.static_api_params["scale"] += 0.1

                    response = requests.get(self.STATIC_API_LINK, params=self.static_api_params)

                    if response:
                        self.map_file = "map.png"
                        with open(self.map_file, "wb") as file:
                            file.write(response.content)
                        file.close()
                    self.set_map()
                else:
                    print("warning")

        elif event.key() == Qt.Key_PageDown:  # Key_PageUp:
            if self.image.text() != "Место не найдено":
                if self.static_api_params["scale"] > 1:
                    self.static_api_params["scale"] -= 0.1

                    response = requests.get(self.STATIC_API_LINK, params=self.static_api_params)

                    if response:
                        self.map_file = "map.png"
                        with open(self.map_file, "wb") as file:
                            file.write(response.content)
                        file.close()
                    self.set_map()
                else:
                    print("warning")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = MapWindow()
    map.show()
    sys.exit(app.exec())
