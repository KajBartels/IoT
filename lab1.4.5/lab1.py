import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import *

import serial
import numpy as np

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QFileDialog, QMessageBox
import csv
import os

class Lab1(QMainWindow):
    def mybuttonfunction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.ui.pushButton.setText("Start")
            self.ui.pushButton.setStyleSheet("background-color: green; color: white;")

            self.ui.MplWidget.canvas.axes.clear()       
            self.ui.MplWidget.canvas.draw()

            self.sensor_data = []
            self.time = 0
            self.x_prev = 0
            self.y_prev = 0
            self.z_prev = 0

        else:
            self.ui.pushButton.setText("Stop")
            self.ui.pushButton.setStyleSheet("background-color: red; color: white;")

            self.timer.start(0)

            self.value1 = self.ui.spinBox.value()


    def __init__(self, data):
        QMainWindow.__init__(self)
        self.data = data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("arduino_sensors")
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)       # .ui weghalen als hij de pushbutton niet kan vinden
        self.timer=QTimer()
        self.timer.timeout.connect(self.showPlot)
        self.value1 = 1

        self.sensor_data = []
        self.ui.saveButton.clicked.connect(self.save_data_to_csv)

        self.x_prev = 0
        self.y_prev = 0
        self.z_prev = 0
        self.time = 0

    def showPlot(self):
        if self.time < self.value1:
            x, y, z = data.get_data()
            print(data.get_data())
            self.sensor_data.append((x, y, z))
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.x_prev, x], 'r', linewidth=0.5)
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.y_prev, y], 'b', linewidth=0.5)
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.3], [self.z_prev, z], 'g', linewidth=0.5)
            self.ui.MplWidget.canvas.draw()
            self.x_prev = x
            self.y_prev = y
            self.z_prev = z
            self.time += 0.3

            x_mean, x_std, y_mean, y_std, z_mean, z_std = self.data.mean_update()
            self.ui.textBrowser_1.setText(f"{x_mean:.2f}")
            self.ui.textBrowser_4.setText(f"{x_std:.2f}")
            self.ui.textBrowser_2.setText(f"{y_mean:.2f}")
            self.ui.textBrowser_5.setText(f"{y_std:.2f}")
            self.ui.textBrowser_3.setText(f"{z_mean:.2f}")
            self.ui.textBrowser_6.setText(f"{z_std:.2f}")

    def save_data_to_csv(self):
        if not self.sensor_data:
            QMessageBox.warning(self, "No Data", "There is no data to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        if os.path.exists(file_path):
            confirm = QMessageBox.question(
                self,
                "file exists",
                f"{file_path} already exists. Do you want to overwrite?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm != QMessageBox.Yes:
                return

        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["X", "Y", "Z"])
                writer.writerows(self.sensor_data)
            QMessageBox.information(self, "complete", f"Data saved in {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "error", f"error in saving:\n{str(e)}")


class Accelerometer():
    def __init__(self):
        self.serial_port = serial.Serial('/dev/ttyACM3', 9600)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.x_data = []
        self.y_data = []
        self.z_data = []

    def read_data(self):
        line = self.serial_port.readline().decode('utf-8').strip()
        data = line.split(',')
        if len(data) == 3:
            try:
                self.x = float(data[0])
                self.y = float(data[1])
                self.z = float(data[2])
                self.x_data.append(float(data[0]))
                self.y_data.append(float(data[1]))
                self.z_data.append(float(data[2]))
            except ValueError:
                print("Invalid data received:", line)

    def get_data(self):
        self.read_data()
        return self.x, self.y, self.z

    def mean_update(self):
        mean_x, std_x = np.mean(self.x_data), np.std(self.x_data)
        mean_y, std_y = np.mean(self.y_data), np.std(self.y_data)
        mean_z, std_z = np.mean(self.z_data), np.std(self.z_data)
        return mean_x, std_x, mean_y, std_y, mean_z, std_z
    

    # x, y, z = self.data.get_data()
    
    # Voeg nieuwe waarden toe aan de lijsten
    
    
    # Bereken statistieken
    


if __name__ == "__main__":
    data = Accelerometer()
    app = QApplication([])
    form = Lab1(data)
    print(data.get_data())
    form.show()
    sys.exit(app.exec_())