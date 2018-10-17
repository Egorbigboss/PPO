# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from main import Presenter
import sys




class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.LoadedModuleView = QtWidgets.QLineEdit(self)
        self.LoadedModuleView.setGeometry(1020,470,220,20)
        self.LoadedModuleView.setReadOnly(True)

        self.presenter = Presenter(self)
        self.__init_ui()
        self.__init_connect()

        self.presenter.restore_data()

    def __init_ui(self):
        self.setGeometry(100,100, 1300, 500)
        self.setWindowTitle('GPX Viewer')
        self.OpenButton = QtWidgets.QPushButton("Импорт",self)
        self.OpenButton.move(10,0)

        self.DeleteGPXButton = QtWidgets.QPushButton("Удалить",self)
        self.DeleteGPXButton.move(130,0)

        self.AddGPXButton = QtWidgets.QPushButton("Добавить",self)
        self.AddGPXButton.move(390,0)

        self.DeletePointButton = QtWidgets.QPushButton("Удл",self)
        self.DeletePointButton.setGeometry(530,350,40,40)

        self.ChangeGPXButton = QtWidgets.QPushButton("Изменить", self)
        self.ChangeGPXButton.move(260, 0)

        self.AddPointButton = QtWidgets.QPushButton("Доб",self)
        self.AddPointButton.setGeometry(590,350,40,40)

        self.FromPolyLineButton = QtWidgets.QPushButton("Из polyline в коорд.", self)
        self.FromPolyLineButton.setGeometry(650, 440, 150, 20)

        self.ToPolyLineButton = QtWidgets.QPushButton("В polyline из коорд.", self)
        self.ToPolyLineButton.setGeometry(650, 470, 150, 20)

        self.UndoBatton = QtWidgets.QPushButton("Отмена",self)
        self.UndoBatton.move(10,400)

        self.RedoBatton = QtWidgets.QPushButton("Повторить",self)
        self.RedoBatton.move(130,400)

        self.GPXTable = QtWidgets.QTableWidget(self)
        self.GPXTable.setColumnCount(3)
        self.GPXTable.setHorizontalHeaderLabels(["Название","Длина","Дата создания"])
        self.GPXTable.setGeometry(10,40,400,300)

        self.PointTable = QtWidgets.QTableWidget(self)
        self.PointTable.setColumnCount(3)
        self.PointTable.setHorizontalHeaderLabels(["Широта","Долгота","Высота"])
        self.PointTable.setGeometry(420,40,350,300)

        self.GPXTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PointTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.PolyLineEdit = QtWidgets.QLineEdit(self)
        self.PolyLineEdit.setGeometry(420,440,220,20)

        self.GraphButton = QtWidgets.QPushButton("График высоты", self)
        self.GraphButton.move(520, 0)

        self.ChangePointButton = QtWidgets.QPushButton("Изм", self)
        self.ChangePointButton.setGeometry(470, 350, 40, 40)

        self.PolyLineView = QtWidgets.QLineEdit(self)
        self.PolyLineView.setGeometry(420,470,220,20)
        self.PolyLineView.setReadOnly(True)




    def __init_connect(self):
        self.OpenButton.clicked.connect(self.presenter.open_file_clicked)
        self.DeleteGPXButton.clicked.connect(self.presenter.delete_gpx_clicked)
        self.ChangeGPXButton.clicked.connect(self.presenter.change_gpx_clicked)
        self.AddGPXButton.clicked.connect(self.presenter.add_gpx_clicked)

        self.GPXTable.cellClicked.connect(self.presenter.row_clicked)
        self.UndoBatton.clicked.connect(self.presenter.undo_clicked)
        self.RedoBatton.clicked.connect(self.presenter.redo_clicked)

        self.DeletePointButton.clicked.connect(self.presenter.delete_points_clicked)
        self.ChangePointButton.clicked.connect(self.presenter.change_point_clicked)
        self.AddPointButton.clicked.connect(self.presenter.add_point_clicked)
        
        self.ToPolyLineButton.clicked.connect(self.presenter.to_polyline_clicked)
        self.FromPolyLineButton.clicked.connect(self.presenter.from_polyline_clicked)
        self.GraphButton.clicked.connect(self.presenter.graphplot_clicked)
    def closeEvent(self, QCloseEvent):
        self.presenter.close_with_save()
        super().closeEvent(QCloseEvent)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = UI()
    MainWindow.show()

    sys.exit(app.exec_())
