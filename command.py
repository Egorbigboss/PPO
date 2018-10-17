from PyQt5 import QtWidgets
from copy import deepcopy



class TableData():
    def __init__(self, row_index = None, type = None, rows = []):
        self.type = type
        self.row_index = row_index
        self.i = None
        self.j = None
        self.data = None
        self.rows = rows





class Command:
	def execute(self):
		raise NotImplementedError()
	def cancel(self):
		raise NotImplementedError()		







class RmCommand(Command):
    def __init__(self,index,datalist,type):
        self.datalist = datalist
        self.index = index
        self.rows = [] 
        self.type = type

    def execute(self):
        self.working_data()
    def cancel(self):
        self.restore_data()

    def working_data(self):
        self.object = self.datalist[self.index]
        del self.datalist[self.index]

    def restore_data(self):
        self.datalist.insert(self.index,self.object)

class AddCommand(Command):
    def __init__(self,row, datalist, row_index,type):
        self.datalist = datalist
        self.index = row_index
        self.type = type

    def execute(self):
        self.__working_data()

    def cancel(self):
        self.__restore_data()


    def __restore_table(self):
        self.table.removeRow(self.index)

    def __restore_data(self):
        del self.datalist[self.index]

    def __create_row(self):
        N = self.table.columnCount()
        M = self.table.rowCount()
        self.table.insertRow(self.index)
        for j in range(N):
            cell = self.rows[j]
            self.table.setItem(self.index,j,QtWidgets.QTableWidgetItem(str(cell)))

    def __working_data(self):
        self.datalist.insert(self.index,self.object)

class CngCommand(Command):
    def __init__(self,i,j,type):
        self.i_index = i
        self.j_index = j
        self.type = type
    






class CngCommandGPX(CngCommand):
    def __init__(self,i, j, value, gpx):
        super().__init__(i, j, "gpx")
        self.gpx = gpx

        self.old_data = None
        self.new_data = value
    def execute(self):
        self.__remember_data()
        self.__set_new_value()

    def cancel(self):
        self.__restore_data()

    def __set_new_value(self):
        if self.j_index == 0: #name
            self.gpx.set_name(self.new_data)
        elif self.j_index == 1: #descr
            self.gpx.set_describe(self.new_data)
        elif self.j_index == 2: #time
            self.gpx.set_time(self.new_data)

    def __remember_data(self):
        if self.j_index == 0: #name
            self.old_data = self.gpx.get_name()
        elif self.j_index == 1: #descr
            self.old_data = self.gpx.get_describe()
        elif self.j_index == 2: #time
            self.old_data = self.gpx.get_time()
        
    def __restore_data(self):
        if self.j_index == 0: #name
            self.gpx.set_name(self.old_data)
        elif self.j_index == 1: #descr
            self.gpx.set_describe(self.old_data)
        elif self.j_index == 2: #time
            self.gpx.set_time(self.old_data)

class CngCommandPoints(CngCommand):
    def __init__(self,i, j, value, gpx):
        super().__init__(i, j, "points")
        self.gpx = gpx

        self.old_data = None
        self.new_data = float(value)
    def execute(self):
        self.__remember_data()
        self.__set_new_value()

    def cancel(self):
        self.__restore_data()

    def __set_new_value(self):
        tp = deepcopy(self.old_data)
        if self.j_index == 0: #lat
            tp.lat = self.new_data
        elif self.j_index == 1:
            tp.lon = self.new_data
        elif self.j_index == 2:
            tp.ele = self.new_data
        track_way = self.gpx.track.track_segment
        del track_way[self.i_index]
        self.gpx.insert_trackpoint(self.i_index,tp)

    def __remember_data(self):
        self.old_data = self.gpx.get_trackpoint(self.i_index)

    def __restore_data(self):
        track_way = self.gpx.track.track_segment
        del track_way[self.i_index]
        self.gpx.insert_trackpoint(self.i_index,self.old_data)

class AddCommandGPX(AddCommand):
    def __init__(self, object, datalist, index):
        row = self.__init_data(object)
        super().__init__(row, datalist, index, "gpx")
    def __init_data(self,object):
        self.object = object
        rows = []
        rows.append(object.get_name())
        rows.append(object.get_describe())
        rows.append(object.get_time())
        return rows

class AddCommandPoint(AddCommand):
    def __init__(self, object, tablelist, index):
        row = self.__init_data(object)
        super().__init__(row, tablelist, index, "points")
    def __init_data(self,object):
        self.object = object
        rows = []
        rows.append(object.lat)
        rows.append(object.lon)
        rows.append(object.ele)
        return rows


