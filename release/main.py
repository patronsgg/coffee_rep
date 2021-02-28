import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from coffee_rep import addEditCoffeeForm
from coffee_rep import main_back
import sqlite3


class MainWindow(QMainWindow, main_back.Ui_MainWindow):
    def __init__(self, tool):
        super().__init__()
        self.setupUi(self)

        self.tool = tool

        self.reload()

        self.pushButton.clicked.connect(self.add_new)
        self.pushButton_2.clicked.connect(self.change)

    def change(self):
        self.mode = 0
        self.current = self.tableWidget.currentIndex()
        if self.tableWidget.item(self.current.row(), 0) is None:
            return
        self.form = AddChangeForm(self, self.tool)
        self.form.show()

    def add_new(self):
        self.mode = 1
        self.form = AddChangeForm(self, self.tool)
        self.form.show()

    def reload(self):
        total = self.tool.cur.execute('''SELECT * FROM coffee''').fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(total))
        for i in range(len(total)):
            for j in range(len(total[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(total[i][j])))


class AddChangeForm(QMainWindow, addEditCoffeeForm.Ui_EditForm):
    def __init__(self, mw, tool):
        super().__init__()
        self.setupUi(self)

        self.tool = tool
        self.mw = mw

        if mw.mode == 0:
            self.pushButton.setText('Изменить')
            total = self.tool.cur.execute('''SELECT * FROM coffee WHERE id=?''',
                                          (mw.tableWidget.item(mw.current.row(), 0).text(),)).fetchall()
            self.lineEdit.setText(total[0][1])
            self.lineEdit_2.setText(total[0][2])
            self.lineEdit_3.setText(total[0][3])
            self.lineEdit_4.setText(total[0][4])
            self.lineEdit_5.setText(total[0][5])
            self.lineEdit_6.setText(total[0][6])
            self.pushButton.clicked.connect(self.change)
        else:
            self.pushButton.clicked.connect(self.add)

    def change(self):
        values = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                  self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text()]
        if '' in values:
            return
        self.tool.cur.execute('''UPDATE coffee SET title=?, degree_of_roasting=?, type=?, 
        comment=?, price=?, value=? WHERE id=?''', (values[0], values[1], values[2], values[3], values[4], values[5],
                                                    self.mw.tableWidget.item(self.mw.current.row(), 0).text()))
        self.tool.con.commit()
        self.close()

    def add(self):
        values = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                  self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text()]
        if '' in values:
            return
        self.tool.cur.execute('''INSERT INTO coffee (title, degree_of_roasting, type, comment, price, value) 
                VALUES (?, ?, ?, ?, ?, ?)''', (values[0], values[1], values[2], values[3], values[4], values[5]))
        self.tool.con.commit()
        self.close()

    def closeEvent(self, event):
        self.mw.reload()


class SqlMethods:
    def __init__(self):
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(SqlMethods())
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())