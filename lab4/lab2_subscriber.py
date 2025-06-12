import sys
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab2_ui import *

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
import zmq

class Lab1(QMainWindow):
    def mybuttonfunction(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
            self.thread = None

            self.ui.pushButton.setText("Start")
            self.ui.pushButton.setStyleSheet("background-color: green; color: white;")

            

            
            self.time = 0
            self.x_prev = 0
            self.y_prev = 0
            self.z_prev = 0
            self.a_prev = 0
            self.b_prev = 0
            self.c_prev = 0

        else:
            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.draw()
            self.ui.pushButton.setText("Stop")
            self.ui.pushButton.setStyleSheet("background-color: red; color: white;")

            self.thread = SensorReader(self.data)
            self.thread.new_data.connect(self.update_plot)
            self.thread.start()




    def __init__(self, data):
        QMainWindow.__init__(self)
        self.data = data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("arduino_sensors")
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)

        self.accel_data = [["Acceleration Data: "]]
        self.gyro_data = [["Gyroscope Data: "]]

        self.ui.saveButton.clicked.connect(self.save_data_to_csv)

        self.thread = None

        self.x_prev = 0
        self.y_prev = 0
        self.z_prev = 0
        self.a_prev = 0
        self.b_prev = 0
        self.c_prev = 0
        self.time = 0



    def update_plot(self, x, y, z, a, b, c):
        self.accel_data.append((x, y, z))
        self.gyro_data.append((a, b, c))
        if self.ui.checkBox_x.isChecked():
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.1], [self.x_prev, x], 'r', linewidth=0.5)
        if self.ui.checkBox_y.isChecked():
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.1], [self.y_prev, y], 'b', linewidth=0.5)
        if self.ui.checkBox_z.isChecked():
            self.ui.MplWidget.canvas.axes.plot([self.time, self.time + 0.1], [self.z_prev, z], 'g', linewidth=0.5)
        if self.ui.checkBox_a.isChecked():
            self.ui.MplWidget_2.canvas.axes.plot([self.time, self.time + 0.1], [self.a_prev, a], 'r', linewidth=0.5)
        if self.ui.checkBox_b.isChecked():
            self.ui.MplWidget_2.canvas.axes.plot([self.time, self.time + 0.1], [self.b_prev, b], 'b', linewidth=0.5)
        if self.ui.checkBox_c.isChecked():
            self.ui.MplWidget_2.canvas.axes.plot([self.time, self.time + 0.1], [self.c_prev, c], 'g', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()
        self.ui.MplWidget_2.canvas.draw()

        self.x_prev = x
        self.y_prev = y
        self.z_prev = z
        self.a_prev = a
        self.b_prev = b 
        self.c_prev = c
        self.time += 0.1


    def save_data_to_csv(self):
        if len(self.accel_data) <= 1 or len(self.gyro_data) <= 1:
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
                writer.writerows(self.accel_data)
                writer.writerow("\n")
                writer.writerows(self.gyro_data)
            QMessageBox.information(self, "complete", f"Data saved in {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "error", f"error in saving:\n{str(e)}")


class Accelerometer():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0

    def read_data(self):
        try:
            while True:
                socket.recv(zmq.NOBLOCK)
        except zmq.Again:
            pass

        md = socket.recv_json()
        array = socket.recv(copy=True)
        data = np.frombuffer(array, dtype=md['dtype']).reshape(md['shape'])
        if len(data) == 6:
            try:
                self.x = float(data[0])
                self.y = float(data[1])
                self.z = float(data[2])
                self.a = float(data[3])
                self.b = float(data[4])
                self.c = float(data[5])
            except ValueError:
                print("Invalid data received:", data)


    def get_data(self):
        self.read_data()
        return self.x, self.y, self.z, self.a, self.b, self.c
    
class SensorReader(QThread):
    new_data = pyqtSignal(float, float, float, float, float, float)

    def __init__(self, accelerometer):
        super().__init__()
        self.accelerometer = accelerometer
        self.running = True

    def run(self):
        self.running = True
        while self.running:
            x, y, z, a, b, c = self.accelerometer.get_data()
            self.new_data.emit(x, y, z, a, b, c)
            self.msleep(100)

    
    def stop(self):
        self.running = False
        self.quit()
        self.wait()



if __name__ == "__main__":
    url = "tcp://127.0.0.1:5558"
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(url)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.setsockopt(zmq.CONFLATE, 1)
    data = Accelerometer()
    app = QApplication([])
    form = Lab1(data)
    print(data.get_data())
    form.show()
    sys.exit(app.exec_())