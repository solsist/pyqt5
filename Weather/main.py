# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import numpy as np
import pymysql
import random
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QSplineSeries, QLineSeries, QChart, QChartView, QValueAxis
from PyQt5.QtCore import Qt, QEasingCurve, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib

from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QVBoxLayout, QWidget, QSlider, QSpinBox

"""
# 插入数据
conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="weather")
cursor = conn.cursor()

# 创建数据表
sql = "CREATE TABLE IF NOT EXISTS contents (id INT AUTO_INCREMENT PRIMARY KEY, max_temp INT, min_temp INT)"
cursor.execute(sql)
datalist = []
for i in range(1, 1578241):
    templist = []
    a = random.randint(10, 30)
    b = random.randint(10, 30)
    max_temp = max(a, b)
    min_temp = min(a, b)

    templist.append(i)
    templist.append(max_temp)
    templist.append(min_temp)
    datalist.append(templist)

insert_sql = "insert into contents values(%s, %s, %s)"
cursor.executemany(insert_sql, datalist)
conn.commit()
conn.close()
cursor.close()
"""


# 计算两个日期间隔分钟
def diff(day1, day2):
    time_array1 = time.strptime(day1, "%Y-%m-%d")
    timestamp_day1 = int(time.mktime(time_array1))
    time_array2 = time.strptime(day2, "%Y-%m-%d")
    timestamp_day2 = int(time.mktime(time_array2))
    result = (timestamp_day2 - timestamp_day1) // 60
    return result


# 日期合法验证
def check_date(s_year, s_month, s_day, s_hour, s_minute, e_year, e_month, e_day, e_hour, e_minute):
    if (s_month == 2 or s_month == 4 or s_month == 6 or s_month == 9 or s_month == 11) and (s_day == 31):
        return False
    if (s_month == 2) and (s_day == 30 or s_day == 29):
        return False
    if (e_month == 2 or e_month == 4 or e_month == 6 or e_month == 9 or e_month == 11) and (e_day == 31):
        return False
    if (e_month == 2) and (e_day == 30 or e_day == 29):
        return False
    if s_year > e_year:
        return False
    if s_year == e_year:
        if s_month > e_month:
            return False
    if s_year == e_year and s_month == e_month:
        if s_day > e_day:
            return False
    if s_year == e_year and s_month == e_month and s_day == e_day:
        if s_hour > e_hour:
            return False
    if s_year == e_year and s_month == e_month and s_day == e_day and s_hour == e_hour:
        if s_minute > e_minute:
            return False

    return True


# 主界面
class MyLegendWidget(QWidget):

    def __init__(self, parent=None):
        super(MyLegendWidget, self).__init__(parent)
        self.e_index = 0
        self.s_index = 0
        self.max_temp = []
        self.min_temp = []
        self.x_data = []
        self.setWindowTitle("气温变化曲线图")
        self.resize(1000, 800)

        self.initUi()

    def initUi(self):
        label_start = QtWidgets.QLabel(self)
        label_start.setText("开始时间")

        label_end = QtWidgets.QLabel(self)
        label_end.setText("结束时间")

        label1 = QtWidgets.QLabel(self)
        label1.setText("年")

        self.comboBox1 = QtWidgets.QComboBox(self)
        self.comboBox1.addItems(["2019", "2020", "2021"])

        label2 = QtWidgets.QLabel(self)
        label2.setText("月")
        self.comboBox2 = QtWidgets.QComboBox(self)
        self.comboBox2.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

        label3 = QtWidgets.QLabel(self)
        label3.setText("日")
        self.comboBox3 = QtWidgets.QComboBox(self)
        self.comboBox3.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                                 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28",
                                 "29", "30", "31"])

        label4 = QtWidgets.QLabel(self)
        label4.setText("时")
        self.comboBox4 = QtWidgets.QComboBox(self)
        self.comboBox4.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                 "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])

        label5 = QtWidgets.QLabel(self)
        label5.setText("分")
        self.comboBox5 = QtWidgets.QComboBox(self)
        self.comboBox5.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                 "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
                                 "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41",
                                 "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55",
                                 "56", "57", "58", "59"])

        label6 = QtWidgets.QLabel(self)
        label6.setText("年")
        self.comboBox6 = QtWidgets.QComboBox(self)
        self.comboBox6.addItems(["2019", "2020", "2021"])

        label7 = QtWidgets.QLabel(self)
        label7.setText("月")
        self.comboBox7 = QtWidgets.QComboBox(self)
        self.comboBox7.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

        label8 = QtWidgets.QLabel(self)
        label8.setText("日")
        self.comboBox8 = QtWidgets.QComboBox(self)
        self.comboBox8.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                                 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28",
                                 "29", "30", "31"])

        label9 = QtWidgets.QLabel(self)
        label9.setText("时")
        self.comboBox9 = QtWidgets.QComboBox(self)
        self.comboBox9.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                 "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])

        label10 = QtWidgets.QLabel(self)
        label10.setText("分")
        self.comboBox10 = QtWidgets.QComboBox(self)
        self.comboBox10.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                  "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
                                  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41",
                                  "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55",
                                  "56", "57", "58", "59"])

        self.button = QtWidgets.QPushButton(self)
        self.button.setMaximumWidth(150)
        self.button.setMinimumHeight(50)
        self.button.setText("生成曲线")

        # 创建图表
        self.chart = QChart()
        self.chartView = QChartView(self.chart, self)
        # 主布局
        buttonLayout = QGridLayout()
        self.mainLayout = QGridLayout()
        buttonLayout.addWidget(label_start, 0, 1)
        buttonLayout.addWidget(label_end, 1, 1)
        buttonLayout.addWidget(label1, 0, 3)
        buttonLayout.addWidget(label2, 0, 5)
        buttonLayout.addWidget(label3, 0, 7)
        buttonLayout.addWidget(label4, 0, 9)
        buttonLayout.addWidget(label5, 0, 11)
        buttonLayout.addWidget(label6, 1, 3)
        buttonLayout.addWidget(label7, 1, 5)
        buttonLayout.addWidget(label8, 1, 7)
        buttonLayout.addWidget(label9, 1, 9)
        buttonLayout.addWidget(label10, 1, 11)
        buttonLayout.addWidget(self.comboBox1, 0, 2)
        buttonLayout.addWidget(self.comboBox2, 0, 4)
        buttonLayout.addWidget(self.comboBox3, 0, 6)
        buttonLayout.addWidget(self.comboBox4, 0, 8)
        buttonLayout.addWidget(self.comboBox5, 0, 10)
        buttonLayout.addWidget(self.comboBox6, 1, 2)
        buttonLayout.addWidget(self.comboBox7, 1, 4)
        buttonLayout.addWidget(self.comboBox8, 1, 6)
        buttonLayout.addWidget(self.comboBox9, 1, 8)
        buttonLayout.addWidget(self.comboBox10, 1, 10)
        buttonLayout.addWidget(self.button, 0, 12, 0, 1)

        displayLayout = QGridLayout()
        finaldisplayLayout = QGridLayout()
        self.spinbox = QSpinBox()
        self.spinbox.setMaximumWidth(100)
        self.label11 = QtWidgets.QLabel()
        self.label11.setMaximumWidth(100)
        displayLayout.addWidget(self.spinbox, 0, 1)
        displayLayout.addWidget(self.label11, 0, 2)
        finaldisplayLayout.addLayout(displayLayout, 0, 2)
        self.mainLayout.addLayout(buttonLayout, 2, 0)
        self.mainLayout.addWidget(self.chartView, 0, 0)
        self.mainLayout.addLayout(finaldisplayLayout, 1, 0)
        self.setLayout(self.mainLayout)

        self.button.clicked.connect(self.getdata)

    def getdata(self):
        s_year = int(self.comboBox1.currentText())
        s_month = int(self.comboBox2.currentText())
        s_day = int(self.comboBox3.currentText())
        s_hour = int(self.comboBox4.currentText())
        s_minute = int(self.comboBox5.currentText())

        e_year = int(self.comboBox6.currentText())
        e_month = int(self.comboBox7.currentText())
        e_day = int(self.comboBox8.currentText())
        e_hour = int(self.comboBox9.currentText())
        e_minute = int(self.comboBox10.currentText())

        result = check_date(s_year, s_month, s_day, s_hour, s_minute, e_year, e_month, e_day, e_hour, e_minute)
        if not result:
            messagebox = QtWidgets.QMessageBox(self)
            messagebox.setText("日期错误")
            messagebox.exec()

        # 计算索引
        s_time = self.comboBox1.currentText() + "-" + self.comboBox2.currentText() + "-" + self.comboBox3.currentText()
        e_time = self.comboBox6.currentText() + "-" + self.comboBox7.currentText() + "-" + self.comboBox8.currentText()

        s_diff_day = diff("2019-01-01", s_time)
        e_diff_day = diff("2019-01-01", e_time)

        start_diff_minute = s_hour * 60 + s_minute + 1
        end_diff_minute = e_hour * 60 + e_minute + 1

        self.s_index = s_diff_day + start_diff_minute
        self.e_index = e_diff_day + end_diff_minute

        self.update()

    def drawline(self):
        self.button.setText("生成曲线")
        self.chart.removeAllSeries()
        self.chart.setTitle("气温曲线图")
        self.chart.legend().show()
        spline = QSplineSeries()
        spline.setName("最高温度")
        spline2 = QSplineSeries()
        spline2.setName("最低温度")
        self.current_value = self.spinbox.value()
        if self.current_value == self.total:
            self.start = len(self.x_data) // 100 * 100
            self.end = self.start + len(self.x_data) % 100
        else:
            self.start = (self.current_value-1) * 100
            self.end = self.start + 100

        for i in range(self.start, self.end):
            spline.append(i, self.max_temp[i])
        spline.setPointsVisible(True)
        spline.setPointLabelsFont(QFont(None, 6))
        spline.setPointLabelsColor(Qt.darkRed)
        self.chart.addSeries(spline)

        for j in range(self.start, self.end):
            spline2.append(j, self.min_temp[j])
        spline2.setPointsVisible(True)

        spline2.setPointLabelsFont(QFont(None, 6))
        spline2.setPointLabelsColor(Qt.darkBlue)
        self.chart.addSeries(spline2)
        self.chart.createDefaultAxes()

        self.chart.axes(Qt.Vertical)[0].setRange(5, 35)

        self.chartView.setChart(self.chart)
        # 抗锯齿
        self.chartView.setRenderHint(QPainter.Antialiasing)

    def initdraw(self):

        self.chart.removeAllSeries()
        self.chart.setTitle("气温曲线图")
        self.chart.legend().show()
        spline = QSplineSeries()
        spline.setName("最高温度")
        spline2 = QSplineSeries()
        spline2.setName("最低温度")
        if len(self.x_data) < 100:
            self.start = 0
            self.end = len(self.x_data)
            self.button.setText("生成曲线")
        else:
            self.start = 0
            self.end = 100

        for i in range(self.start, self.end):
            spline.append(i, self.max_temp[i])
        spline.setPointsVisible(True)
        spline.setPointLabelsFont(QFont(None, 6))
        spline.setPointLabelsColor(Qt.darkRed)
        self.chart.addSeries(spline)

        for j in range(self.start, self.end):
            spline2.append(j, self.min_temp[j])
        spline2.setPointsVisible(True)

        spline2.setPointLabelsFont(QFont(None, 6))
        spline2.setPointLabelsColor(Qt.darkBlue)
        self.chart.addSeries(spline2)
        self.chart.createDefaultAxes()

        self.chart.axes(Qt.Vertical)[0].setRange(5, 35)

        self.chartView.setChart(self.chart)
        # 抗锯齿
        self.chartView.setRenderHint(QPainter.Antialiasing)

    def update(self):

        self.button.setText("查询中")
        self.cal = seekThread(self.s_index, self.e_index)
        self.cal.callback.connect(self.update_sum)
        self.cal.start()


    def update_sum(self, r1, r2, r3):

        self.max_temp = r1
        self.min_temp = r2
        self.x_data = r3
        self.button.setText("翻页查看数据")

        self.spinbox.setMinimum(1)
        if len(self.x_data) % 100 != 0:
            self.total = int(len(self.x_data) / 100) + 1
        else:
            self.total = int(len(self.x_data) / 100)
        self.spinbox.setMaximum(self.total)
        self.label11.setText("总共" + str(self.total) + "页")
        self.spinbox.setValue(1)
        self.initdraw()
        self.spinbox.valueChanged.connect(self.drawline)



class seekThread(QThread):
    callback = pyqtSignal(list, list, list)

    def __init__(self, start_index, end_index):
        super().__init__()

        self.x_data = []
        self.min_temp = []
        self.max_temp = []
        self.s_index = start_index
        self.e_index = end_index

    def run(self):
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="weather")
        cursor = conn.cursor()

        sql = "SELECT * FROM contents where id >= %s and id <= %s"
        cursor.execute(sql, (self.s_index, self.e_index))

        fin_result = cursor.fetchall()

        conn.close()
        cursor.close()
        self.x_data = np.arange(0, len(fin_result), 1)
        for j in range(0, len(fin_result)):
            self.max_temp.append(fin_result[j][1])
            self.min_temp.append(fin_result[j][2])

        self.callback.emit(list(self.max_temp), list(self.min_temp), list(self.x_data))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyLegendWidget()
    window.show()
    sys.exit(app.exec())
