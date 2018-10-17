from engine import Engine
from PyQt5 import QtCore, QtGui, QtWidgets


class Presenter():
    def __init__(self, parent):
        self.model = Engine(self, parent)
        self.UI = parent
        self.modules = []
        self.list_modules = []





    def __clear_stack_redo(self):

        self.stack_redo.clear()

    def __get_datagpx_line(self, i_index):
        N = self.UI.GPXTable.columnCount()
        datalist = []
        for j in range(N):
            elem = self.UI.GPXTable.item(i_index,j)
            datalist.append(elem)
        return datalist
    def __get_datapoints_line(self,i_index):
        N = self.UI.PointTable.columnCount()
        datalist = []
        for j in range(N):
            elem = self.UI.PointTable.item(i_index,j)
            datalist.append(elem)
        return datalist

    def __set_cell(self,i,j,data):
        if data is None:
            data = "---"
        else:
            data = str(data)
        self.UI.GPXTable.setItem(i,j,QtWidgets.QTableWidgetItem(data))

    def __fill_points_row(self,index):
        gpx = self.model.get_gpx(index)
        track = gpx.track.track_segment
        N = len(track)
        self.UI.PointTable.setRowCount(N)
        for i in range(N):
            lon = track[i].lon
            lat = track[i].lat
            ele = track[i].ele
            item_lon = QtWidgets.QTableWidgetItem(str(lon))
            item_lat = QtWidgets.QTableWidgetItem(str(lat))
            item_ele = QtWidgets.QTableWidgetItem(str(ele))
            self.UI.PointTable.setItem(i,0,item_lat)
            self.UI.PointTable.setItem(i,1,item_lon)
            self.UI.PointTable.setItem(i,2,item_ele)

    def change_gpx_clicked(self):
        cell = self.UI.GPXTable.currentIndex()
        self.model.change_gpx_clicked(cell)

        
    def change_point_clicked(self):
        index_gpx = self.UI.GPXTable.currentIndex().row()
        cell = self.UI.PointTable.currentIndex()
        
        self.model.change_point_clicked(index_gpx, cell)


    def open_file_clicked(self):
        self.model.stack_redo.clear()
        count = self.model.add_data_from_file()
        if count:
            self.update_gpx_table()


    def update_gpx_table(self):
        N = len(self.model.gpxs)
        self.UI.GPXTable.setRowCount(0) #clear
        self.UI.GPXTable.setRowCount(N)
        for i in range(N):
            gpx = self.model.get_gpx(i)
            self.__set_cell(i,0,gpx.get_name())
            length = "%.2f" % float(gpx.get_describe())
            self.__set_cell(i,1,length)
            self.__set_cell(i,2,gpx.get_time())

        
    def __set_points_table(self,data):
        for i in range(len(data)):
            M = self.UI.PointTable.rowCount()
            self.UI.PointTable.insertRow(M)
            self.UI.PointTable.setItem(M,0,QtWidgets.QTableWidgetItem(str(data[i][0])))
            self.UI.PointTable.setItem(M,1,QtWidgets.QTableWidgetItem(str(data[i][1])))

    def close_with_save(self):

        self.model.save_raw_data()

    def restore_data(self):

        self.model.restore_raw_data()




    def delete_gpx_clicked(self):
        curr_index = self.UI.GPXTable.currentIndex().row()
        self.model.delete_gpx_clicked(curr_index)




    def delete_points_clicked(self):
        gpx_index = self.UI.GPXTable.currentIndex().row()
        curr_index = self.UI.PointTable.currentIndex().row()

        self.model.delete_points_clicked(gpx_index, curr_index)




    def undo_clicked(self):
        self.model.undo_clicked()


    def redo_clicked(self):
        self.model.redo_clicked()



    def row_clicked(self):
        index = self.UI.GPXTable.currentRow()
        self.UI.PointTable.setRowCount(0)
        self.__fill_points_row(index)
        self.UI.PolyLineView.setText("")
        self.UI.PolyLineEdit.setText("")

    def add_point_clicked(self):
        self.model.add_point_clicked()


    def add_gpx_clicked(self):
        self.model.add_gpx_clicked()
        return 


    def to_polyline_clicked(self):
        index = self.UI.GPXTable.currentRow()
        if index > -1:
            text = self.model.convert_to_polyline(index)
            if text is not None:
                self.model.to_polyline(text)

    def from_polyline_clicked(self):
        text = self.model.from_polyline()
        index = self.UI.GPXTable.currentRow()
        if index > -1 and text is not None:
            points = self.model.convert_to_points(index, text)
            if points is not None:
                self.__set_points_table(points)

    def graphplot_clicked(self):
        gpx_index = self.UI.GPXTable.currentIndex().row()
        if gpx_index > -1:
            self.model.plot_graph(gpx_index)

    def update_points_table(self):
        self.UI.PointTable.setRowCount(0)
        gpx_index = self.UI.GPXTable.currentIndex().row()
        self.__fill_points_row(gpx_index)
    
    def get_points_row_number(self):
        return self.UI.PointTable.rowCount()

    def get_gpx_row_number(self):
        return self.UI.GPXTable.rowCount()

    def get_points_horizontal_text(self, j):
        return self.UI.PointTable.horizontalHeaderItem(j).text()

    def get_gpx_horizontal_text(self,j):
        return self.UI.GPXTable.horizontalHeaderItem(j).text()
    def get_current_index(self):
        return self.UI.GPXTable.currentIndex().row()

    def lib_button_clicked(self, buttname):
        index = self.UI.GPXTable.currentIndex().row()
        self.model.start_visitor(buttname, index)
        