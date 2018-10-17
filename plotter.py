import matplotlib.pyplot as plt
from parser_gpx import Track



class Plotter():
    def __init__(self, points):
        self.vertex = points
        

    def setup(self):
        N = len(self.vertex)
        dist = 0
        self.distance = [dist]
        self.elevation = [self.vertex[0].ele]
        for i in range(1,N):
            ele = self.vertex[i].ele
            if ele is None:
                return False
            self.elevation.append(ele)
            A = self.vertex[i - 1]
            B = self.vertex[i]
            dist += Track.distance_from_points(None, A ,B)
            self.distance.append(dist)
        return True
    def plot(self):
        plt.plot(self.distance, self.elevation)
        plt.xlabel('Расстояние (км)')
        plt.ylabel('Высота (м)')
        plt.title('Карта высот')
        plt.grid(True)
        plt.show()



