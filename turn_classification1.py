from copy import deepcopy
from PyQt5 import QtWidgets
from math import sin, cos, radians, atan2, atan, sqrt, degrees, pi, acos

class Track():
    @staticmethod
    def distance_from_points(self,A,B):
        delta_lat = radians(A.lat - B.lat)
        delta_lon = radians(A.lon - B.lon)
        a = sin(delta_lat/2)**2 + cos(radians(A.lat)) * cos(radians(B.lat)) * (sin(delta_lon/2)**2)
        distance = 2 * atan2(sqrt(a), sqrt(1-a)) * 6371 #R = 6371 is radius of the Earth
        return distance

    @staticmethod
    def angle_from_points(self, A, B, tangens_mode = False):
        delta_h = B.ele - A.ele
        delta_l = Track.distance_from_points(None, A, B) * 1000 # k = 1000, to meters
        if delta_l == 0:
            return 0
        tangens = delta_h / delta_l
        if tangens_mode:
            return tangens
        result = atan(tangens)
        return degrees(result)

    @staticmethod
    def turn_angle(self, A, B, C):
        ab = Track.distance_from_points(None, A, B)
        bc = Track.distance_from_points(None, B, C)
        ac = Track.distance_from_points(None, A, C)

        if ab == 0 or bc == 0 or ac == 0:
            return 180

        cos_gamma = (ab*ab + bc*bc - ac*ac)/(2*ab*bc)
        if abs(cos_gamma) > 1:
            return 180

        gamma = acos(cos_gamma)
        return degrees(gamma)





def get_gpx_file(path):
    parser = Parser()
    parser.setup(path)
    gpx = parser.GetData()
    return gpx



class TableTurn():
    def __init__(self, angle_from, angle_to, category):
        self.category = category
        self.angle_from = angle_from
        self.angle_to = angle_to
    def belong(self, angle):
        if self.angle_from <= abs(angle) < self.angle_to:
            return self.category
        else:
            return None




class CounterTurn(TableTurn):
    def __init__(self, category, angle_from, angle_to):
        super().__init__(category, angle_from, angle_to)
        self.count = 0
    def add_one(self):
        self.count += 1





class TurnClassification():
    def __init__(self, **kwargs):
        self.init()
        self.module_name = "turn_classification"
        self.txtwidget = None
    def init(self):
        self.turn_table = [CounterTurn(-0.1,1,-1),
                           CounterTurn(1,6,0),
                           CounterTurn(6,11,1),
                           CounterTurn(11,34,2),
                           CounterTurn(34,56,3),
                           CounterTurn(56,79,4),
                           CounterTurn(79,90,5),
                           CounterTurn(90,135,6),
                           CounterTurn(135,160,7)
                           ]

    def check_category(self, angle):
        N = len(self.turn_table)
        category = None
        for i in range(N):
            category = self.turn_table[i].belong(angle)
            if category is not None:
                break
        return category

    def add_category_one(self, category):
        N = len(self.turn_table)
        for i in range(N):
            if category == self.turn_table[i].category:
                self.turn_table[i].add_one()
                break 

    def classify_old(self, track_segment):
        past_category = 0
        N = len(track_segment)

        for i in range(N-2):
            start = track_segment[i]
            medium = track_segment[i+1]
            stop = track_segment[i+2]
            angle = 180 - Track.turn_angle(None,start,medium, stop)
            curr_category = self.check_category(angle)

            if curr_category != past_category:
                if past_category is None:
                    past_category = curr_category
                    continue
                self.add_category_one(curr_category)
                past_category = curr_category

        d = 3

    def classify(self, track_segment):
        max_cat = -1
        past_category = -1
        N = len(track_segment)


        for i in range(N-2):
            start = track_segment[i]
            medium = track_segment[i+1]
            stop = track_segment[i+2]
            angle = 180 - Track.turn_angle(None,start,medium, stop)
            print("kek")
            curr_category = self.check_category(angle)

            print(curr_category)

            max_cat = max(max_cat, curr_category)
            if curr_category == -1 and past_category != -1:
                self.add_category_one(max_cat)
                max_cat = -1
            past_category = curr_category
        return True


    def ui_init(self, main_window, butt_handler):
        main_window.button_start = QtWidgets.QPushButton("Повороты по категориям",main_window)
        main_window.button_start.setGeometry(1020,70,140,30)
        main_window.text_edit = QtWidgets.QTextEdit(main_window)

        self.txtwidget = main_window.text_edit
        main_window.text_edit.setGeometry(850,40,150,100)
        main_window.text_edit.setReadOnly(True)
        main_window.button_start.clicked.connect(lambda: butt_handler(self.module_name))

    def update_mess(self):
        
        mess = "Типы поворотов: \n"
        N = len(self.turn_table)
        for i in range(1,N):
            mess += "тип %d: %d \n" % (self.turn_table[i].category,self.turn_table[i].count)
        return mess

    def run(self, track_segment):
        self.init()
        mess = ""
        result = self.classify(track_segment)
        print( "bas")
        if result:
            mess = self.update_mess()
        else:
            mess = "Отсутствуют данные о высоте!"
        self.txtwidget.setText(mess)
    def accept(self, visitor):
        visitor.visit(self)

class EModule(TurnClassification):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)






if __name__ == "main":
    A = SignClassificationSlopes()
    gpx = get_gpx_file("route_crimea.gpx")

    seg = gpx.track.track_segment
    A.classify(seg)