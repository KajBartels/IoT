import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import *

class Lab1(QMainWindow):
    def mybuttonfunction(self):
        value1 = self.ui.spinBox.value()
        value2 = self.ui.spinBox_2.value()
        print(f"Value 1: {value1}, Value 2: {value2}")
        
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("arduino_sensors")
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
                        
if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    sys.exit(app.exec_())