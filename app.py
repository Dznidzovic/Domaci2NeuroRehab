import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from SerialComm import SerialComunication
from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QComboBox, QLabel, QLineEdit
import pyqtgraph as pg


class App(QtWidgets.QMainWindow):

    def startRead(self):
        if not self.start:
            self.start = True
        
    def stopRead(self):
        if self.start:
            self.start = False

    def updateData(self):
        if self.start:
            curentData = self.ser_port.read_line()
            if  curentData:
                self.xAxis = self.xAxis[1:]
                self.xAxis.append(self.xAxis[-1] + 0.00625)

                self.yAxis = self.yAxis[1:]
                self.yAxis.append(curentData[self.combox.currentIndex()])

                self.classX = self.classX[1:]
                self.classX.append(self.classX[-1] + 0.00625)

                self.classY = self.classY[1:]
                self.classY.append(curentData[-1])


                self.signal_plot.setData(self.xAxis, self.yAxis)
                self.class_plot.setData(self.classX, self.classY)
            

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        
        self.start = False
        self.startTime = 5

        self.xAxis = list(np.linspace(0.0, 5.0, num=800))
        self.yAxis = [0 for _ in range(800)]

        self.classX = list(np.linspace(0.0, 5.0, num=800))
        self.classY = [0 for _ in range(800)]

        self.setWindowTitle("App")
        self.layout = QGridLayout()
       
        self.button = QPushButton('Start')
        self.button.setMaximumSize(150, 50)
        self.button.setMinimumSize(150, 50)
        self.layout.addWidget(self.button, 0, 0)
        self.button.clicked.connect(self.startRead)

        self.button = QPushButton('Stop')
        self.button.setMaximumSize(150, 50)
        self.button.setMinimumSize(150, 50)
        self.layout.addWidget(self.button, 0, 1)
        self.button.clicked.connect(self.stopRead)

        self.combox = QComboBox()
        self.combox.setMaximumSize(150, 50)
        self.combox.setMinimumSize(150, 50)
        for i in range(24):
            self.combox.addItem("CH" + str(i + 1))

        self.combox.setCurrentIndex(0)
        self.layout.addWidget(self.combox, 0, 2)

        self.graphWidgetEEG = pg.PlotWidget()        
        self.graphWidgetEEG.setMaximumSize(700, 300)
        self.graphWidgetEEG.setMinimumSize(700, 300)
        self.graphWidgetEEG.setYRange(-500, 500, padding=0)
        self.layout.addWidget(self.graphWidgetEEG, 1, 0)

        self.graphWidgetMovement = pg.PlotWidget()
        self.graphWidgetMovement.setMaximumSize(700, 300)
        self.graphWidgetMovement.setMinimumSize(700, 300)
        self.graphWidgetMovement.setYRange(3, 1, padding=0)
        self.layout.addWidget(self.graphWidgetMovement, 1, 1)
        

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.signal_plot =  self.graphWidgetEEG.plot(self.xAxis, self.yAxis)
        self.class_plot = self.graphWidgetMovement.plot(self.classX, self.classY)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.updateData)
        self.timer.start()

        self.ser_port = SerialComunication()
        self.ser_port.turn_simulator_on()
        self.ser_port.activate_channel(255)
        

    def __del__(self):
        self.ser_port.turn_simulator_off()

app = QtWidgets.QApplication(sys.argv)
w = App()
w.show()
sys.exit(app.exec_())