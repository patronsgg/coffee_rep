import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        total = cur.execute('''SELECT * FROM coffee''').fetchall()

        self.tableWidget.setRowCount(len(total))
        for i in range(len(total)):
            for j in range(len(total[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(total[i][j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())