import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import *

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Lab1(QMainWindow):
    def mybuttonfunction(self):
        value2 = self.ui.spinBox_2.value()
        self.timer.start(value2 * 1000)
        value1 = self.ui.spinBox.value()
        print(f"Value 1: {value1}, Value 2: {value2}")
        if value1 > self.begin:
            self.y.extend(map(lambda x: x**2, range(self.begin +1, value1 + 1)))
        else:
            self.y = list(map(lambda x: x**2, range(0, value1 + 1)))
        self.begin = value1

    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("arduino_sensors")
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.begin = 1
        self.y = [0]
        self.timer=QTimer()
        self.timer.timeout.connect(self.showPlot)

    def showPlot(self):
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(range(len(self.y)), self.y, 'r', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()


        
                        
if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    sys.exit(app.exec_())