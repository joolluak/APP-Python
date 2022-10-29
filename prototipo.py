from cmath import e
from PyQt5.QtSql import QSqlDatabase
import sqlite3
from tkinter import *
from struct import unpack
from collections import deque
from colorama import Cursor
import matplotlib.pyplot as plt
import threading
import serial
import pandas as pd
from scipy import signal
import sys
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from random import randint


ID = 11
SIZE = 28
FORMAT = '<BHHHHHHHHBBBBBBBLB'

car = deque(200 * [''], 200)
accx = deque(200 * [0], 200)
accy = deque(200 * [0], 200)
accz = deque(200 * [0], 200)
rpm = deque(200 * [0], 200)
speed = deque(200 * [0], 200)
temp_motor = deque(200 * [0], 200)
flags = deque(200 * [0], 200)
soc = deque(200 * [0], 200)
temp_cvt = deque(200 * [0], 200)
volt = deque(200 * [0], 200)
latitude = deque(200 * [0], 200)
longitude = deque(200 * [0], 200)
timestamp = deque(200 * [0], 200)
eixo = deque(200 * [0], 200)

b, a = signal.butter(1, 0.1, analog=False)

car_save = []
accx_save = []
accy_save = []
accz_save = []
rpm_save = []
speed_save = []
temp_motor_save = []
flags_save =[]
soc_save = []
temp_cvt_save = []
volt_save = []
latitude_save = []
longitude_save = []
timestamp_save = []


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class Receiver(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.com = self.connectSerial(serial_ports())
        print(f'Connected into {self.com}')

    def connectSerial(self, USB_PORT):
        com = []
        for usb in USB_PORT:
            try:
                com = serial.Serial(f'{usb}', 115200)
            except:
                print("Tentativa...")
                com = []
            if com:
                break

        if not com:
            raise Exception("Não há nenhuma porta serial disponível")
        else:
            return com

    def run(self):
        self.com.flush()

        while True:
            try:
                self.checkData()
            except:
                break

    #database stuff
    con = sqlite3.connect('TelemetriaBaja.db')
    cr = con.cursor()

    def checkData(self):
        c = 0
        while c != b'\xff':
            c = self.com.read()
            # print(f'trying, {c}')
        msg = self.com.read(SIZE)
        # print(msg)
        pckt = list(unpack(FORMAT, msg))
        # print(pckt)
        # print((pckt[25]/65535)*5000)
        if pckt[0] == 22:
            car.append("MB2")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            longitude.append(pckt[15])
            timestamp.append(pckt[16])

            car_save.append("MB2")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])

        if pckt[0] == 11:
            car.append("MB1")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            longitude.append(pckt[15])
            timestamp.append(pckt[16])

            car_save.append("MB1")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])

        data = {
            'Tempo': timestamp_save,
            'Carro': car_save,
            'Aceleração X': accx_save,
            'Aceleração Y': accy_save,
            'Aceleração Z': accz_save,
            'RPM': rpm_save,
            'Velocidade': speed_save,
            'Temperatura do motor': temp_motor_save,
            'Temperatura da CVT': temp_cvt_save,
            'State of Charge' : soc_save

        }
        csv = pd.DataFrame(data , columns=['Tempo', 'Carro', 'Aceleração X', 'Aceleração Y', 'Aceleração Z', 'RPM',
                                          'Velocidade', 'Temperatura do motor', 'Temperatura da CVT', 'State of Charge' ])
        #csv.to_csv('dados_telemetria.csv')
    
    #con.execute('''INSERT INTO TelemetriaBaja VALUES('car', 'accx', 'accy', 'accz', 'rpm', 'speed', 
     #           'temp_motor', 'flags', 'soc', 'temp_cvt', 'volt', 'latitude', 'longitude', 'timestamp' )''') 
    
    #cursor = con.execute('''SELECT * FROM TelemetriaBaja    ''')
    df = pd.read_sql_table("SELECT * from TelemetriaBaja", con)
    print(df.head())
    con.commit()
    con.close()

    def dbConnection():
        database = 'TelemetriaBaja.db'
        try:
            connection = sqlite3.connect(database)
            db_cursor = connection.cursor()
            db_cursor.execute('''SELECT * FROM TelemetriaBaja   ''')
            rows = db_cursor.fetchall()
            for row in rows:
                print(row)
            connection.close()
        except sqlite3.Error:
            print("Error in connection")
        db_cursor.connection.close()


class Ui_MainWindow(object):
    def __init__(self):
        self.webView = QWebEngineView()
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 459)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.map = QVBoxLayout(self.centralwidget)
        self.map.setGeometry(QtCore.QRect(10, 10, 461, 251))
        self.map.setObjectName("map")

        self.graph_rot = pg.PlotWidget(self.centralwidget)
        self.graph_rot.setGeometry(QtCore.QRect(10, 290, 221, 150))
        self.graph_rot.setObjectName("graph_rot")
        self.graph_rot.setBackground('w')
        self.graph_rot.plot(timestamp_save,rpm_save)
        self.graph_rot.setTitle("RPM", color='r')

        self.graph_vel = pg.PlotWidget(self.centralwidget)
        self.graph_vel.setGeometry(QtCore.QRect(250, 290, 221, 150))
        self.graph_vel.setObjectName("graph_vel")
        self.graph_vel.setBackground('w')
        self.graph_vel.plot(timestamp_save, speed_save)
        self.graph_vel.setTitle("Velocidade", color='b')

        font = QtGui.QFont()
        font.setPointSize(16)

        self.acc_x = QtWidgets.QLabel(self.centralwidget)
        self.acc_x.setGeometry(QtCore.QRect(510, 10, 101, 51))
        self.acc_x.setObjectName("acc_x")
        self.acc_x.setFont(font)

        self.acc_y = QtWidgets.QLabel(self.centralwidget)
        self.acc_y.setGeometry(QtCore.QRect(640, 10, 101, 51))
        self.acc_y.setObjectName("acc_y")
        self.acc_y.setFont(font)

        self.acc_z = QtWidgets.QLabel(self.centralwidget)
        self.acc_z.setGeometry(QtCore.QRect(770, 10, 101, 51))
        self.acc_z.setObjectName("acc_z")
        self.acc_z.setFont(font)

        self.fuel = QtWidgets.QLabel(self.centralwidget)
        self.fuel.setGeometry(QtCore.QRect(510, 60, 161, 200))
        self.fuel.setObjectName("fuel")
        self.fuel.setText("")
        self.fuel.setPixmap(QtGui.QPixmap("fuel_empty.jpg"))
        self.fuel.setScaledContents(True)

        self.batt = QtWidgets.QLabel(self.centralwidget)
        self.batt.setGeometry(QtCore.QRect(690, 110, 161, 101))
        self.batt.setObjectName("batt")
        self.batt.setFont(font)

        self.temp_motor = QtWidgets.QLabel(self.centralwidget)
        self.temp_motor.setGeometry(QtCore.QRect(690, 240, 161, 101))
        self.temp_motor.setObjectName("temp_motor")
        self.temp_motor.setFont(font)

        self.temp_cvt = QtWidgets.QLabel(self.centralwidget)
        self.temp_cvt.setGeometry(QtCore.QRect(510, 240, 161, 101))
        self.temp_cvt.setObjectName("temp_cvt")
        self.temp_cvt.setFont(font)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(570, 370, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 370, 101, 31))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 19))
        self.menubar.setObjectName("menubar")
        self.menuOp_es = QtWidgets.QMenu(self.menubar)
        self.menuOp_es.setObjectName("menuOp_es")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.menuOp_es.addAction(self.actionStart)
        self.menuOp_es.addAction(self.actionStop)
        self.menubar.addAction(self.menuOp_es.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_plots(self, rot_x, rot_y, vel_x, vel_y):
        self.rpm_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.vel_pen = pg.mkPen(color=(0, 0, 255), width=2)
        self.dataline_rpm = self.graph_rot.plot(rot_x, rot_y, pen=self.rpm_pen)
        self.dataline_vel = self.graph_vel.plot(vel_x, vel_y, pen=self.vel_pen)

    def update_random(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.


        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.dataline_rpm.setData(self.x, self.y)  # Update the data.
        self.dataline_vel.setData(self.x, self.y)  # Update the data.

    def update_map(self, coordinate):

        self.m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=15,
            location=coordinate
        )
        folium.Marker(location=coordinate).add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webView.setFixedWidth(461)
        self.webView.setFixedHeight(251)
        self.webView.setHtml(self.data.getvalue().decode())

        self.map.addWidget(self.webView, 0, QtCore.Qt.AlignTop)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mangue Telemetria"))

        self.update_map((-8.05428, -34.8813))
        self.update_plots([0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4])
        self.acc_x.setText(_translate("MainWindow", "Acc x = 0g"))
        self.acc_y.setText(_translate("MainWindow", "Acc y = 0g"))
        self.acc_z.setText(_translate("MainWindow", "Acc z = 0g"))
        self.batt.setText(_translate("MainWindow", "Bateria = 0%"))
        self.temp_motor.setText(_translate("MainWindow", "Motor = 0ºC"))
        self.temp_cvt.setText(_translate("MainWindow", "CVT = 0ºC"))
        self.comboBox.setItemText(0, _translate("MainWindow", "BOX"))
        self.pushButton.setText(_translate("MainWindow", "Enviar"))
        self.menuOp_es.setTitle(_translate("MainWindow", "Opções"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_random)
        self.timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.acc_x.setText('Acc: x = 1g')
    ui.acc_y.setText('Acc: y = 2g')
    ui.acc_z.setText('Acc: z = 3g')
    ui.batt.setText('Bateria: 10%')
    ui.temp_motor.setText('Motor: 30°')
    ui.temp_cvt.setText('CVT:30°')
    #exemplo: ui.acc_x.setText("Acc x = 2g")
    sys.exit(app.exec_())

