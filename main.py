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
        self.data.move(50, 150)
        self.data.resize(500, 300)


        self.jobs = QListWidget(self)
        self.jobs.setGeometry(QRect(600, 100, 530, 400))
        self.jobs.setStyleSheet("font:12pt;")
        self.jobs.setObjectName("jobs")




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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
