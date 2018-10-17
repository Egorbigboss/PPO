ыfrom PyQt5 import QtWidgets
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



class TableSteepnessLengthSlopes():
    def __init__(self, tangens_from, tangens_to, length, name):
        # tangens = (real tangens) * 100
        self.tangens_from = tangens_from
        self.tangens_to = tangens_to
        self.name = name
        self.minlength = length
    def belong_tangens(self, angle):
        if (self.tangens_from <= abs(angle) < self.tangens_to):
            return True, self.name
        else:
            return False, None

    def belong_length(self, length):
        if (length > self.minlength):
            return True
        else:
            return False




class CounterSteepnessLengthSlopes(TableSteepnessLengthSlopes):
    def __init__(self, angle_from, angle_to, minlength,name):
        super().__init__(angle_from, angle_to,minlength, name)
        self.count = 0
    def add_one(self):
        self.count += 1




class SignClassificationSlopes():
    def __init__(self, **kwargs):
        self.init()
        self.module_name = "sign_classification_slopes"
        self.txtwidget = None
    def init(self):
        self.table_steepness_length_slopes = [CounterSteepnessLengthSlopes(40,50,600,0),
                                        CounterSteepnessLengthSlopes(50,60,450,1),
                                        CounterSteepnessLengthSlopes(60,70,350,2),
                                        CounterSteepnessLengthSlopes(70,80,300,3),
                                        CounterSteepnessLengthSlopes(80,4294967295,270,4),
                                       ]


    def add_steepness_one(self, name):
        N = len(self.table_steepness_length_slopes)
        result = False
        for i in range(N):
            if name == self.table_steepness_length_slopes[i].name:
                self.table_steepness_length_slopes[i].add_one()
                break
                    


    def check_steepness_slopes(self, tangens):
        N = len(self.table_steepness_length_slopes)
        name = None
        for i in range(N):
            result, name = self.table_steepness_length_slopes[i].belong_tangens(tangens)
            if result:
                break
        return name

    def check_length_slopes(self, name, length):
        N = len(self.table_steepness_length_slopes)
        result = False
        for i in range(N):
            if name == self.table_steepness_length_slopes[i].name:
                if self.table_steepness_length_slopes[i].belong_length(length):
                    result = True
                else:
                    result = False
                break
        return result

    def classify(self, track_segment):
        past_name = None
        N = len(track_segment)
        length = 0
        #for first
        for i in range(N-1):
            start = track_segment[i]
            stop = track_segment[i+1]
            if start.ele == None or stop.ele == None:
                return False
            tangens = Track.angle_from_points(None, start, stop, True) * 100 #проценты
            name_steepness = self.check_steepness_slopes(tangens)


            if name_steepness != past_name:
                if past_name is None:
                    past_name = name_steepness
                    continue

                if self.check_length_slopes(name_steepness,length):
                    self.add_steepness_one(name_steepness)

                length = 0
                past_name = name_steepness
            else:
                length += Track.distance_from_points(None, start, stop) * 1000
        return True


    def accept(self, visitor):
        visitor.visit(self)

    def ui_init(self, main_window, butt_handler):
        main_window.button_start1 = QtWidgets.QPushButton("Количество знаков",main_window)
        main_window.button_start1.setGeometry(1020,180,140,30)
        main_window.text_edit1 = QtWidgets.QTextEdit(main_window)
        self.txtwidget = main_window.text_edit1
        main_window.text_edit1.setGeometry(850,150,150,100)
        main_window.text_edit1.setReadOnly(True)
        main_window.button_start1.clicked.connect(lambda: butt_handler(self.module_name))

    def update_mess(self):
        mess = "Типы знаков: \n"
        for x in self.table_steepness_length_slopes:
            mess += "Уклон %d: %d \n" % (x.tangens_from, x.count)
        return mess
    def run(self, track_segment):
        self.init()
        mess = ""
        result = self.classify(track_segment)
        if result:
            mess = self.update_mess()
        else:
            mess = "Отсутствуют данные о высоте!"
        self.txtwidget.setText(mess)



class EModule(SignClassificationSlopes):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)