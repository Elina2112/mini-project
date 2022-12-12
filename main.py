import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QTime, QRect
from PyQt5.QtGui import QPainter, QColor
from random import choice, randint
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, \
    QGraphicsOpacityEffect, QDialog, QMessageBox, QTableView, QDateEdit, QDateTimeEdit, QListWidgetItem, QListWidget, \
    QCalendarWidget
from PyQt5.QtGui import QPixmap
import sqlite3

conn = sqlite3.connect('planirovshik.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Plan(
Id INTEGER PRIMARY KEY AUTOINCREMENT,
Data varchar(30),
Time_start varchar(30),
Time_end varchar(30),
Job varchar(30),
Status_Job varchar(30))
""")
conn.commit()

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 1200, 700)
        self.setWindowTitle('Планировщик на день')
        self.spisokt = QLabel('Список дел', self)
        self.spisokt.setStyleSheet("font:12pt;")
        self.spisokt.adjustSize()
        self.spisokt.move(800, 30)

        self.datat = QLabel('Выберите дату', self)
        self.datat.setStyleSheet("font:12pt;")
        self.datat.adjustSize()
        self.datat.move(250, 30)

        self.pixmap = QPixmap("1.jpg").scaled(1200, 700)
        self.image = QLabel(self)
        self.image.resize(1200, 700)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)
        self.image.setGraphicsEffect(self.opacity_effect)
        self.image.setPixmap(self.pixmap)



        self.data = QCalendarWidget(self)
        self.data.setObjectName("Дата")
        self.data.setStyleSheet("font:10pt;")
        self.data.move(50, 150)
        self.data.resize(500, 300)


        self.jobs = QListWidget(self)
        self.jobs.setGeometry(QRect(600, 100, 530, 400))
        self.jobs.setStyleSheet("font:12pt;")
        self.jobs.setObjectName("jobs")

        self.jobt = QLabel('Введите дело', self)
        self.jobt.setStyleSheet("font:10pt;")
        self.jobt.adjustSize()
        self.jobt.move(800, 510)
        self.job = QLineEdit(self)
        self.job.setObjectName("Дело")
        self.job.move(600, 550)
        self.job.resize(530, 40)

        self.time_startt = QLabel('Время начала', self)
        self.time_startt.move(100, 480)
        self.time_startt.setStyleSheet("font:10pt;")
        self.time_startt.adjustSize()
        self.time_start = QDateTimeEdit(QTime.currentTime(), self)
        self.time_start.setObjectName("Время начала")
        self.time_start.move(100, 510)
        self.time_start.resize(170, 30)

        self.time_endt = QLabel('Время конца', self)
        self.time_endt.move(320, 480)
        self.time_endt.setStyleSheet("font:10pt;")
        self.time_endt.adjustSize()
        self.time_end = QDateTimeEdit(QTime.currentTime(), self)
        self.time_end.setObjectName("Время конца")
        self.time_end.move(320, 510)
        self.time_end.resize(170, 30)


        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("planirovshik.sqlite")
        self.db.open()
        self.view = QTableView(self)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Plan')
        self.model.select()
        self.view.setModel(self.model)
        self.view.move(50, 60)
        self.view.resize(0, 0)

        self.button_1 = QPushButton(self)
        self.button_1.move(650, 620)
        self.button_1.resize(170, 30)
        self.button_1.setText("Добавить дело")
        self.button_1.clicked.connect(self.run1)

        self.button_2 = QPushButton(self)
        self.button_2.move(900, 620)
        self.button_2.resize(170, 30)
        self.button_2.setText("Удалить дело")
        #self.button_2.clicked.connect(self.run2)

    def run1(self):
        conn = sqlite3.connect("planirovshik.sqlite")
        cur = conn.cursor()

        j = str(self.job.text())
        ts=str(self.time_start.text())
        te= str(self.time_end.text())
        d = self.data.selectedDate().toPyDate()

        cur.execute('''INSERT INTO Plan(Data, Time_start, Time_end,Job, Status_Job) VALUES (?, ?, ?,?,?)''',(d, ts, te, j, "Не выполнено"))
        conn.commit()

        msg = QMessageBox()
        msg.setWindowTitle("Успешно")
        msg.setText("Успешно добавлено")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.job.clear()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


