from PyQt5 import QtCore, QtGui, QtWidgets
from plotter import Plotter
from parser_gpx import Gpx_parser, GPX, TrackPoint, Track
import pickle
from library_checker import LibraryChecker
from visitor import Visitor
from command import RmCommand, AddCommandGPX, CngCommandGPX, CngCommandPoints, AddCommandPoint, TableData
import polyline









class Engine():
    def __init__(self, parent, ui):
        self.presenter = parent
        self.gpxs = [] 
        self.parser = Gpx_parser()
        self.stack_undo = []
        self.stack_redo = []

        check = LibraryChecker(["morphological_classification_slopes","sign_classification_slopes","turn_classification"])
        self.loaded_modules, self.name_loaded_modules = check.load_modues()
        self.connect_modules(ui)

    def connect_modules(self,ui):
        self.active_modules = []
        for mod in self.loaded_modules:
            m = mod.EModule()
            m.ui_init(ui,self.presenter.lib_button_clicked)
            self.active_modules.append(m)

        txt = ""
        for mod in self.name_loaded_modules: 
            txt += mod + "; "
        ui.LoadedModuleView.setText(txt)



    def undo_clicked(self):
        if len(self.stack_undo):
            command = self.stack_undo.pop()
            command.cancel()
            if command.type == "gpx":
                self.presenter.update_gpx_table()
            elif command.type == "points":
                self.presenter.update_points_table()
            self.stack_redo.append(command)

    def redo_clicked(self):
        if len(self.stack_redo):
            command = self.stack_redo.pop()
            command.execute()
            if command.type == "gpx":
                self.presenter.update_gpx_table()
            elif command.type == "points":
                self.presenter.update_points_table()
            self.stack_undo.append(command)

    def add_gpx_clicked(self):
        
        data = self.add_gpx_core()
        if self.gpx_field_validator(data):
            self.stack_redo.clear()
            gp = GPX()
            gp.track = Track()
            gp.set_describe(data[1])
            gp.set_name(data[0])
            gp.set_time(data[2])
            N = self.presenter.get_gpx_row_number()
            command = AddCommandGPX(gp,self.gpxs, N)
            command.execute()
            self.presenter.update_gpx_table()
            self.stack_undo.append(command)


    def add_point_clicked(self):

        gpx_index = self.presenter.get_current_index()
        if gpx_index > -1:
            data = self.add_point_core()
            if self.points_field_validator(data):
                self.stack_redo.clear()
                tp = TrackPoint(data[0],data[1], elevation = data[2])
                datalist = self.get_gpx(gpx_index).track.track_segment
                N = self.presenter.get_points_row_number()
                command = AddCommandPoint(tp,datalist,N)
                command.execute()
                self.presenter.update_points_table()

                self.stack_undo.append(command)


    def delete_points_clicked(self,gpx_index,curr_index  ):
        if gpx_index > -1 and curr_index > -1:
            self.stack_redo.clear()
            datalist = self.get_gpx(gpx_index)
            command = RmCommand(curr_index, datalist.track.track_segment, "points")
            command.execute()
            self.presenter.update_points_table()
            self.stack_undo.append(command)

    def delete_gpx_clicked(self, curr_index):
        if curr_index > -1:
            self.stack_redo.clear()
            datalist = self.gpxs
            command = RmCommand(curr_index, datalist, "gpx")
            command.execute()
            self.presenter.update_gpx_table()
            self.stack_undo.append(command)


    def change_gpx_clicked(self, cell):
        self.stack_redo.clear()
        i = cell.row()
        if i > -1:
            j = cell.column()
            colname = self.presenter.get_gpx_horizontal_text(j)
            data = cell.data()
            data = self.change_gpx_core(colname,data)
            old_data = data
            if j == 1: #length
                data = self.double_validator(data)
            elif j == 2: #date
                data = self.date_validator(data)

            if data is not None:
                curr_gpx = self.get_gpx(i)
                command = CngCommandGPX(i,j,data,curr_gpx)
                command.execute()
                self.presenter.update_gpx_table()

                self.stack_undo.append(command)
        
    def change_point_clicked(self,index_gpx,cell):
        i = cell.row()
        if index_gpx > -1 and i > -1:
            self.stack_redo.clear()
            j = cell.column()
            colname = self.presenter.get_points_horizontal_text(j)
            data = cell.data()
            data = self.change_gpx_core(colname,data)
            data = self.double_validator(data)
            if data is not None:
                command = CngCommandPoints(i,j,data,self.get_gpx(index_gpx))
                command.execute()
                self.presenter.update_points_table()
                self.stack_undo.append(command)


    def __get_gpx_file(self,path):
        self.parser.setup(path)
        gpx = self.parser.GetData()
        if gpx is not None:
            self.gpxs.append(gpx)
        return gpx

    def delete_gpx(self,index):

        del self.gpxs[index]

    def change_gpx_core(self,colname,data):
        text, ok = QtWidgets.QInputDialog.getText(self.presenter.UI, 'Изменение',colname,text = data)
        if ok:
            data = text
        return data
    def get_gpx(self,index):

        return self.gpxs[index]
    def get_points(self,gpx_index,point_index):

        return self.get_gpx(gpx_index).get_trackpoint(point_index)

    def add_gpx_core(self):
        text, ok = QtWidgets.QInputDialog.getText(self.presenter.UI, 'Добавление','Название,длина,время')
        data = text.split(',')
        return data

    def add_point_core(self):
        text, ok = QtWidgets.QInputDialog.getText(self.presenter.UI, 'Добавление','Широта, Долгота, Высота')

        data = text.split(',')
        return data

    def convert_to_polyline(self,index):
        gpx = self.get_gpx(index)
        track_segment = gpx.track.track_segment
        if (len(track_segment)):
            line = [(obj.lat, obj.lon) for obj in track_segment]
            my_polyline = polyline.encode(line)
        else:
            return None
        return my_polyline

    def convert_to_points(self,index,data):
        try:
            points = polyline.decode(data)
        except:
            self.show_warning("При конвертации полилайна произошла ошибка!")
            return None
        gpx = self.get_gpx(index)
        track_segment = gpx.track.track_segment
        for pnt in points:
            pt = TrackPoint(pnt[0],pnt[1])
            track_segment.append(pt)
        return points

    def add_data_from_file(self):
        window = QtWidgets.QFileDialog()
        window.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        data = window.getOpenFileNames(self.presenter.UI,"Открыть файл",'',"GPS eXchange (*.gpx)")
        list_files = data[0]
        count = len(list_files)
        for path in list_files:
            if (len(path) == 0):
                return 0
            else:
                result  = self.__get_gpx_file(path)
                if result is None:
                    count -= 1
                    del path
                    self.show_warning("Один/несколько файлов повреждены!")

        return count

    def double_validator(self,data):
        number = data
        try:
            number = float(data)
        except ValueError:
            number  = None
        return number
    def date_validator(self,data):
        dtlist = data.split('.')
        if (len(dtlist) == 3):
            for x in dtlist:
                try:
                    int(x)
                except ValueError:
                    return None
            return data
        return None
    
    def coordinate_validtor(self,x):
        result = True
        if x > 180 or x < -180:
            result = False
        return result
         
    
    def gpx_field_validator(self,text):
        result = False
        if (len(text) == 3):
            if self.date_validator(text[2]) is not None and \
                self.double_validator(text[1]) is not None:
                result = True
        return result


    def points_field_validator(self,text):
        result = False
        if (len(text) == 3):
            text[0] = self.double_validator(text[0])
            text[1] = self.double_validator(text[1])
            text[2] = self.double_validator(text[2])
            if text[0] is not None and \
               text[1] is not None:
                result = True
        return result
    def show_warning(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Предупреждение")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()

    def save_raw_data(self):
        try:
            with open("gpxs.pickle", 'wb') as f:
                pickle.dump(self.gpxs,f)
        except:
            return
    def restore_raw_data(self):
        try:
            with open("gpxs.pickle", 'rb') as f:
                self.gpxs = pickle.load(f)
            self.presenter.update_gpx_table()
        except:
            return

    def to_polyline(self,data):
        filename = QtWidgets.QFileDialog.getSaveFileName(self.presenter.UI,"Экспорт polyline","Result.plln",filter ="Google Polyline (*.plln)")
        if len(filename[0]) == 0:
            return
        f = open(filename[0],'w')
        print(data,file = f)
        f.close()

    def from_polyline(self):
        window = QtWidgets.QFileDialog()
        filename = window.getOpenFileName(self.presenter.UI,"Импорт polyline",'',"Google Polyline (*.plln)")
        if len(filename[0]) == 0:
            return None
        f = open(filename[0],'r')
        data = f.read()
        f.close()
        return data[:-1]

    def plot_graph(self, index):
        gpx = self.get_gpx(index)
        points = gpx.track.track_segment

        plot = Plotter(points)
        result = plot.setup()
        if result:
            plot.plot()
        else:
            self.show_warning("Нехватает данных о высоте!")
        

    def start_visitor(self, module_name, index_gpx):
        track_seg = self.gpxs[index_gpx].track.track_segment
        v = Visitor(track_seg)
        N = len(self.loaded_modules)
        for i in range(N):
            if module_name == self.active_modules[i].module_name:
                self.active_modules[i].accept(v)
                


