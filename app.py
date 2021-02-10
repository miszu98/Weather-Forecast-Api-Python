from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QPalette, QImage
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QBrush
import requests
import sys
import time

class Weather_checker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather")
        self.config()
        self.gps_location()
        self.background_image()
        self.show()

    def config(self):
        self.mainLayout = QGridLayout()

        #info
        self.itemp = QLabel('None', self)
        self.itemp.setGeometry(QRect(0,60, 500, 100))
        self.itemp.setAlignment(Qt.AlignCenter)
        self.itemp.setObjectName("celsjus")
        self.itemp.setStyleSheet("QLabel#celsjus {color: white}")


        c_bold = QFont()
        c_bold.setPointSize(11)
        c_fontsize = QFont()
        c_fontsize.setPointSize(60)
        self.itemp.setFont(c_fontsize)

        self.akt_czas = QLabel("None",self)
        self.idate = QLabel('Last Update: ', self)
        self.akt_czas.setGeometry(QRect(50,190,500,100))
        self.akt_czas.setAlignment(Qt.AlignCenter)
        self.idate.setGeometry(QRect(180, 190, 500, 100))
        self.setWindowIcon(QIcon("Aplikacja_pogody/weather-icon.png"))
        self.setFixedSize(500, 400)
        self.akt_czas.setFont(c_bold)
        self.idate.setFont(c_bold)
        self.idate.setObjectName("idate")
        self.idate.setStyleSheet("QLabel#idate {color: white}")
        self.akt_czas.setObjectName("akt_czas")
        self.akt_czas.setStyleSheet("QLabel#akt_czas {color: white}")

        self.pressure = QLabel("Current Pressure", self)
        self.ipressure = QLabel("None", self)
        self.ipressure.setGeometry(QRect(350,160, 460-350, 100))
        self.ipressure.setAlignment(Qt.AlignCenter)
        self.pressure.setGeometry(QRect(350,130, 300, 100))
        self.pressure.setFont(c_bold)
        self.ipressure.setFont(c_bold)
        self.ipressure.setObjectName("ipressure")
        self.ipressure.setStyleSheet("QLabel#ipressure {color: white}")
        self.pressure.setObjectName("pressure")
        self.pressure.setStyleSheet("QLabel#pressure {color: white}")

        self.humidity = QLabel("Current Humidity", self)
        self.ihumidity = QLabel("None", self)
        self.ihumidity.setGeometry(QRect(210, 160, 320-210, 100))
        self.ihumidity.setAlignment(Qt.AlignCenter)
        self.humidity.setGeometry(QRect(210, 130, 300, 100))
        self.humidity.setFont(c_bold)
        self.ihumidity.setFont(c_bold)
        self.ihumidity.setObjectName("ihumidity")
        self.ihumidity.setStyleSheet("QLabel#ihumidity {color: white}")
        self.humidity.setObjectName("humidity")
        self.humidity.setStyleSheet("QLabel#humidity {color: white}")

        self.weather = QLabel("Weather Description", self)
        self.iweather = QLabel("None", self)
        self.iweather.setGeometry(QRect(46, 160, 175-46, 100))
        self.iweather.setAlignment(Qt.AlignCenter)
        self.weather.setGeometry(QRect(45,130, 300, 100))
        self.weather.setFont(c_bold)
        self.iweather.setFont(c_bold)
        self.iweather.setObjectName("iweather")
        self.iweather.setStyleSheet("QLabel#iweather {color: white}")
        self.weather.setObjectName("weather")
        self.weather.setStyleSheet("QLabel#weather {color: white}")

        # Edit Line
        self.search = QLineEdit(self)
        self.search.setFixedSize(140, 25)
        c = self.search.font()
        c.setPointSize(12)
        self.search.setFont(c)
        self.search.move(10, 10)

        # Search Button
        self.btn_search = QPushButton('Search', self)
        self.btn_search.setFixedSize(50, 25)
        self.btn_search.move(155, 10)

        self.btn_search.clicked.connect(self.fill_info)
        self.setLayout(self.mainLayout)

    def get_info(self):
        api = "d6072614c06005c471c66bdc8935f97b"
        url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city = self.search.text()
        fill = url + "appid=" + api + "&q=" + self.city
        response = requests.get(fill)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            self.current_temperature = str(round(y["temp"] - 273.15, 1)) + "℃"
            self.current_pressure = y["pressure"]
            self.current_humidity = y["humidity"]
            z = x["weather"]
            self.weather_description = z[0]["description"]
            return self.current_temperature,self.current_pressure,self.current_humidity,self.weather_description
        else:
            self.search.setText("")
            QMessageBox.warning(self, "Not Exist", 'City/Country does not exist !')

    def fill_info(self):
        if self.search.text() != "":
            self.itemp.setText(self.get_info()[0])
            self.ipressure.setText(str(self.get_info()[1]) + " hPa" )
            self.ihumidity.setText(str(self.get_info()[2]) + "%")
            self.iweather.setText(str(self.get_info()[3]))
        else:
            QMessageBox.warning(self, 'Empty field', 'You must fill field city/country.')

        date = time.localtime()
        akt = list(date[3:6])
        for x in range(0, len(akt)):
            if len(str(akt[x])) == 1:
                akt[x] = '0' + str(akt[x])
            else:
                akt[x] = str(akt[x])
        self.akt_czas.setText(":".join(akt))

    def gps_location(self):
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        your_city = data['city']
        self.search.setText(str(your_city))
        self.btn_search.click()

    def background_image(self):
        self.img = QImage("Aplikacja_pogody/weather_img/bg_app.jpg")
        self.scaled_img = self.img.scaled(QSize(500, 400))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.scaled_img))
        self.setPalette(self.palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    okno = Weather_checker()
    sys.exit(app.exec_())
