import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import *

import serial

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Lab1(QMainWindow):
    def mybuttonfunction(self):
        if (self.timer.isActive()):
            self.timer.stop()
            print("stop")
        else:
            value2 = self.ui.spinBox_2.value()
            self.timer.start(value2 * 1000)
            value1 = self.ui.spinBox.value()
            print(f"Value 1: {value1}, Value 2: {value2}")
            if value1 > self.begin:
                self.y.extend(map(lambda x: x**2, range(self.begin +1, value1 + 1)))
            else:
                self.y = list(map(lambda x: x**2, range(0, value1 + 1)))
            self.begin = value1

    def __init__(self, data):
        QMainWindow.__init__(self)
        self.data = data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("arduino_sensors")
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.begin = 1
        self.y = [0]
        self.timer=QTimer()
        self.timer.timeout.connect(self.showPlot)
        self.x_prev = 0
        self.y_prev = 0
        self.z_prev = 0
        self.time = 0

    def showPlot(self):
        x, y, z = data.get_data()
        print(data.get_data())
        data.clear_data()
        # self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.x_prev, x], 'r', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.y_prev, y], 'b', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.z_prev, z], 'g', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()
        self.x_prev = x
        self.y_prev = y
        self.z_prev = z
        self.time += 0.3

class Accelerometer():
    def __init__(self):
        self.serial_port = serial.Serial('/dev/ttyACM3', 9600)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0        # x hoeft mischien niet 0 te zijn omdat de kracht op de arduino nooit 0 is

    def read_data(self):
        line = self.serial_port.readline().decode('utf-8').strip()
        data = line.split(',')
        if len(data) == 3:
            try:
                self.x = float(data[0])
                self.y = float(data[1])
                self.z = float(data[2])
            except ValueError:
                print("Invalid data received:", line)

    def get_data(self):
        self.read_data()
        return self.x, self.y, self.z
    
    def clear_data(self):
        self.x = 0
        self.y = 0
        self.z = 0



if __name__ == "__main__":
    data = Accelerometer()
    app = QApplication([])
    form = Lab1(data)
    print(data.get_data())
    form.show()
    sys.exit(app.exec_())