import unittest
from random import randint, choice
import time
import command
import string
from parser_gpx import TrackPoint, Track, GPX
import polyline
from copy import deepcopy
import pickle
from plotter import Plotter

class PolylineCodecTestCase(unittest.TestCase):

    def test_decode_multiple_points(self):
        d = polyline.decode('gu`wFnfys@???nKgE??gE?????oK????fE??fE')
        self.assertEqual(d, [
            (40.641, -8.654),
            (40.641, -8.654),
            (40.641, -8.656),
            (40.642, -8.656),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.641, -8.653),
            (40.641, -8.654)
        ])

    def test_decode_multiple_points_precision(self):
        d = polyline.decode('o}oolA~ieoO???~{Bo}@??o}@?????_|B????n}@??n}@', 6)
        self.assertEqual(d, [
            (40.641, -8.654),
            (40.641, -8.654),
            (40.641, -8.656),
            (40.642, -8.656),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.641, -8.653),
            (40.641, -8.654)
        ])

    def test_decode_official_example(self):
        d = polyline.decode('_p~iF~ps|U_ulLnnqC_mqNvxq`@')
        self.assertEqual(d, [
            (38.500, -120.200),
            (40.700, -120.950),
            (43.252, -126.453)
        ])

    def test_decode_official_example_precision(self):
        d = polyline.decode('_izlhA~rlgdF_{geC~ywl@_kwzCn`{nI', 6)
        self.assertEqual(d, [
            (38.500, -120.200),
            (40.700, -120.950),
            (43.252, -126.453)
        ])

    def test_decode_single_point(self):
        d = polyline.decode('gu`wFf`ys@')
        self.assertEqual(d, [
            (40.641, -8.653)
        ])

    def test_decode_single_point_precision(self):
        d = polyline.decode('o}oolAnkcoO', 6)
        self.assertEqual(d, [
            (40.641, -8.653)
        ])

    def test_encode_multiple_points(self):
        e = polyline.encode([
            (40.641, -8.654),
            (40.641, -8.654),
            (40.641, -8.656),
            (40.642, -8.656),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.641, -8.653),
            (40.641, -8.654)
        ])
        self.assertEqual(e, 'gu`wFnfys@???nKgE??gE?????oK????fE??fE')

    def test_encode_multiple_points_precision(self):
        e = polyline.encode([
            (40.641, -8.654),
            (40.641, -8.654),
            (40.641, -8.656),
            (40.642, -8.656),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.655),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.642, -8.653),
            (40.641, -8.653),
            (40.641, -8.654)
        ], 6)
        self.assertEqual(e, 'o}oolA~ieoO???~{Bo}@??o}@?????_|B????n}@??n}@')

    def test_encode_official_example(self):
        e = polyline.encode([
            (38.500, -120.200),
            (40.700, -120.950),
            (43.252, -126.453)
        ])
        self.assertEqual(e, '_p~iF~ps|U_ulLnnqC_mqNvxq`@')

    def test_encode_official_example_precision(self):
        e = polyline.encode([
            (38.500, -120.200),
            (40.700, -120.950),
            (43.252, -126.453)
        ], 6)
        self.assertEqual(e, '_izlhA~rlgdF_{geC~ywl@_kwzCn`{nI')

    def test_encode_single_point(self):
        e = polyline.encode([
            (40.641, -8.653)
        ])
        self.assertEqual(e, 'gu`wFf`ys@')

    def test_encode_single_point_rounding(self):
        e = polyline.encode([
            (0, 0.000006),
            (0, 0.000002)
        ])
        self.assertEqual(e, '?A?@')

    def test_rounding_py3_match_py2(self):
        e = polyline.encode([
            (36.05322, -112.084004),
            (36.053573, -112.083914),
            (36.053845, -112.083965)])
        self.assertEqual(e, 'ss`{E~kbkTeAQw@J')

    def test_encode_single_point_precision(self):
        e = polyline.encode([
            (40.641, -8.653)
        ], 6)
        self.assertEqual(e, 'o}oolAnkcoO')

    def test_a_variety_of_precisions(self):
      

        def generator():
            while True:
                coords = []
                for i in range(2, randint(4, 10)):
                    lat, lon = uniform(-180.0, 180.0), uniform(-180.0, 180.0)
                    coords.append((lat, lon))
                yield coords

        patience = 3  # seconds.
        waypoints, okays = 0, 0

        g = generator()
        start = time.time()
        while time.time() < start + patience:
            precision = randint(4, 8)
            wp = next(g)
            waypoints += len(wp)
            poly = polyline.encode(wp, precision)
            wp2 = polyline.decode(poly, precision)
            if wp == wp2:
                okays += len(wp2)
            else:
                for idx, _ in enumerate(wp):
                    dx, dy = abs(wp[idx][0] - wp2[idx][0]), abs(wp[idx][1] - wp2[idx][1])
                    if dx > 10 ** -(precision - 1) or dy > 10 ** -(precision - 1):
                        print("idx={}, dx={}, dy={}".format(idx, dx, dy))
                    else:
                        okays += 1

        assert okays == waypoints
        print("encoded and decoded {0:.2f}% correctly for {1} waypoints @ {2} wp/sec".format(
            100 * okays / float(waypoints),
            waypoints,
            round(waypoints / patience, 0)))




class AddPointsTestCase(unittest.TestCase):
    def setup(self, N):
        self.N = N
        self.track_segment = []
        for i in range(N):
            tp = TrackPoint(randint(-180,180),randint(-180,180),randint(-10000,10000))
            self.track_segment.append(tp)

    def test_add_single_point(self, start_val = 5):
        self.setup(start_val)
        benchmark_data = deepcopy(self.track_segment)

        tp = TrackPoint(123,456,789)
        comm = command.AddCommandPoint(tp, self.track_segment, self.N)
        comm.execute()   
        benchmark_data.append(deepcopy(tp))       
        

        self.assertTrue(len(self.track_segment) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.track_segment[i] , benchmark_data[i] )

    def test_add_multi_point(self, start_val = 5, count_value = 2):
        self.setup(start_val)
        benchmark_data = deepcopy(self.track_segment)

        for i in range(count_value):
            self.N = len(self.track_segment)
            tp = TrackPoint(randint(-180,180),randint(-180,180),randint(-10000,10000))
            comm = command.AddCommandPoint(tp, self.track_segment, self.N)
            comm.execute() 
            benchmark_data.append(deepcopy(tp))       

        self.assertTrue(len(self.track_segment) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.track_segment[i] , benchmark_data[i] )


class AddGPXTestCase(unittest.TestCase):

    def __get_random_string(self,min_char = 8, max_char = 12):
        allchar = string.ascii_letters + string.punctuation + string.digits
        st = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        return st

    def __gen_gpx(self, data = None):
        if data is None:
            data = [self.__get_random_string(),randint(1, 1000),"%d.%d.%d" % (randint(1, 30),randint(1, 12),randint(1970, 2018)) ]
        gp = GPX()
        gp.track = Track()
        gp.set_describe(data[0])
        gp.set_name(data[1])
        gp.set_time(data[2])
        return gp

    def __setup(self, N):
        self.N = N
        self.gpxs = []
        for i in range(N):
            tp = self.__gen_gpx()
            self.gpxs.append(tp)

    def test_add_single_gpx(self, start_val = 5):
        self.__setup(start_val)
        benchmark_data = deepcopy(self.gpxs)

        gp = GPX()
        gp.track = Track()
        gp.set_describe("Test1")
        gp.set_name("123")
        gp.set_time("1.01.1970")
        comm = command.AddCommandGPX(gp, self.gpxs, self.N)
        comm.execute()   
        benchmark_data.append(deepcopy(gp)) 

        self.assertTrue(len(self.gpxs) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.gpxs[i] , benchmark_data[i] )
            
    def test_add_multiple_gpx(self, start_val = 5, count_value = 2):
        self.__setup(start_val)
        benchmark_data = deepcopy(self.gpxs)

        for i in range(count_value):
            self.N = len(self.gpxs)
            gp = self.__gen_gpx()
            comm = command.AddCommandGPX(gp, self.gpxs, self.N)
            comm.execute()   
            benchmark_data.append(deepcopy(gp)) 

        self.assertTrue(len(self.gpxs) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.gpxs[i] , benchmark_data[i] )


class DeleteGPXTestCase(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        self.default_data = None

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
                self.default_data = pickle.load(f)


    def test_single_gpx_delete(self):
        self.setUp()
        index = 1
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.RmCommand(index, self.default_data, "gpx")
        cmnd.execute()
        del benchmark_list[index]

        self.assertCountEqual(benchmark_list, self.default_data)
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)
        
    def test_multiple_gpx_delete(self):
        self.setUp()
        index1 = 2
        index2 = 0
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.RmCommand(index1, self.default_data, "gpx")
        cmnd.execute()
        cmnd = command.RmCommand(index2, self.default_data, "gpx")
        cmnd.execute()

        del benchmark_list[index1]
        del benchmark_list[index2]

        self.assertCountEqual(benchmark_list, self.default_data)
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)      
            
             
    def test_delete_from_empty(self):
        index = 1
        cmnd = command.RmCommand(index, self.default_data, "gpx")
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)
        
class DeletePointsTestCase(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        self.default_data = None

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.default_data = gpxs[2].track.track_segment


    def test_single_point_delete(self):
        self.setUp()
        index = 1
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.RmCommand(index, self.default_data, "points")
        cmnd.execute()
        del benchmark_list[index]

        

        self.assertTrue(len(benchmark_list) == len(self.default_data))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)
        
    def test_multiple_point_delete(self):
        self.setUp()
        index1 = 2
        index2 = 0
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.RmCommand(index1, self.default_data, "points")
        cmnd.execute()
        cmnd = command.RmCommand(index2, self.default_data, "points")
        cmnd.execute()

        del benchmark_list[index1]
        del benchmark_list[index2]

        self.assertTrue(len(benchmark_list) == len(self.default_data))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)      
            
             
    def test_delete_from_empty(self):
        index = 1
        cmnd = command.RmCommand(index, self.default_data, "points")
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)
     
class ChangePointsTestCase(unittest.TestCase):
    def __init__(self, columnname = 'lat',methodName = 'runTest'):
        self.default_data = None
        self.column_index = 0
        self.colname = columnname
        if columnname == 'lat':
            self.column_index = 0
        elif columnname == 'lon':
            self.column_index = 1
        elif columnname == 'ele':
            self.column_index = 2
        else:
            raise ValueError("This type of column not found")

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.default_data = gpxs[2]



    def __manual_change(self,index,value, benchmark_list):
        columnname = self.colname
        if columnname == 'lat':
            benchmark_list[index].lat = float(value)
        elif columnname == 'lon':
            benchmark_list[index].lon = float(value)
        elif columnname == 'ele':
            benchmark_list[index].ele = float(value)


    def test_point_change(self):
        self.setUp()
        index = 1
        value = "12345"
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.CngCommandPoints(index,self.column_index, value,self.default_data)
        cmnd.execute()
        
        

        benchmark_list = benchmark_list.track.track_segment
        self.__manual_change(index, value, benchmark_list)

        working_list = self.default_data.track.track_segment

        self.assertTrue(len(working_list) == len(benchmark_list))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == working_list[i]
            self.assertTrue(cond)
        
        
    def test_multiple_point_change(self):
        self.setUp()
        index1 = 1
        index2 = 10
        value1 = "12345"
        value2 = "321"
        benchmark_list = deepcopy(self.default_data)
        cmnd = command.CngCommandPoints(index1,self.column_index, value1, self.default_data)
        cmnd.execute()
        cmnd = command.CngCommandPoints(index2,self.column_index, value2, self.default_data)
        cmnd.execute()

        
        

        benchmark_list = benchmark_list.track.track_segment
        self.__manual_change(index1, value1, benchmark_list)
        self.__manual_change(index2, value2, benchmark_list)

        working_list = self.default_data.track.track_segment

        self.assertTrue(len(working_list) == len(benchmark_list))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == working_list[i]
            self.assertTrue(cond)  
            
             

    def test_change_notexisting(self):
        self.setUp()
        index = 100000
        value = "12345"
        cmnd = command.CngCommandPoints(index,self.column_index, value,self.default_data)
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)

class PlotterTestCase(unittest.TestCase):
    def setUp(self, index):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        return gpxs[index]

    def test_plot_exist_data(self):
        gpx = self.setUp(2)
        points = gpx.track.track_segment

        plot = Plotter(points)
        result = plot.setup()
        self.assertTrue(result)

    def test_plot_not_exist_data(self):
        gpx = self.setUp(1)
        points = gpx.track.track_segment

        plot = Plotter(points)
        result = plot.setup()
        self.assertFalse(result)


class RestoreConditionTestCase(unittest.TestCase):

    def test_empty_list(self):
        gpxs = None
        with open("restoretest0.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == 0)

    def test_single_list(self):
        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("111")
        benchmark_gpx.set_name("test1")
        benchmark_gpx.set_time("1.01.2000")
        gpxs = None
        benchmark_gpxs = [benchmark_gpx]

        with open("restoretest1.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == len(benchmark_gpxs))
        self.assertTrue(gpxs[0] == benchmark_gpxs[0])

    def test_multi_list(self):
        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("111")
        benchmark_gpx.set_name("test1")
        benchmark_gpx.set_time("1.01.2000")
        benchmark_gpxs = [benchmark_gpx]

        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("222")
        benchmark_gpx.set_name("test2")
        benchmark_gpx.set_time("2.02.2000")

        benchmark_gpxs.append(benchmark_gpx)
        gpxs = None
        with open("restoretest2.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == len(benchmark_gpxs))
        for i in range(len(gpxs)):
            self.assertTrue(gpxs[i] == benchmark_gpxs[i])
        

d = RestoreConditionTestCase()
d.test_single_list()

