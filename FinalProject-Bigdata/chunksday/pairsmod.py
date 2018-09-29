from mrjob.job import MRJob
import datetime as dt
import csv
#import numpy as np
#from mrjob.step import MRStep
#from mr3px.csvprotocol import CsvProtocol
#import os
#import sys
# generated using head -n 5000 yellow_tripdata_2016-08.csv >> first.csv

gap=1/23
def line_eq(line):
    # line is a list of two tuples, each representing an end point
    x1, y1 = line[0]
    x2, y2 = line[1]
    if x1 - x2 == 0:
        return None, x1
    slope = (y1 - y2) / (x1 - x2)
    c = y1 - slope * x1
    return slope, c

def interior(line, point):
    # line is a list of two tuples, each representing an end point
    # point is a tuple
    x_lst = [line[0][0], line[1][0]]
    y_lst = [line[0][1], line[1][1]]
    if point[0] < min(x_lst) or point[0] > max(x_lst):
        return False
    if point[1] < min(y_lst) or point[1] > max(y_lst):
        return False
    return True

def intersect(line1, line2):
    m1, c1 = line_eq(line1)
    m2, c2 = line_eq(line2)
    rv = []
    # if line1 is vertical:
    if m1 is None:
        if m2 is None:
            if c1 != c2:
                return rv
            lst = sorted([line1[0][1], line1[1][1], line2[0][1], line2[1][1]])
            i = 0
            while lst[1] + i * gap < lst[2] + gap / 2:
                rv.append((c1, lst[1] + i * gap))
                i += 1
            return rv
        
        x = c1
        y = m2 * x + c2
        if interior(line1, (x, y)) and interior(line2, (x, y)):
            rv.append((x, y))
        return rv
    
    # if line2 is vertical    
    if m2 is None:
        if m1 is None:
            if c1 != c2:
                return rv
            
            lst = sorted([line1[0][1], line1[1][1], line2[0][1], line2[1][1]])
            i = 0
            while lst[1] + i * gap < lst[2] + gap / 2:
                rv.append((c2, lst[1] + i * gap))
                i += 1
            return rv
        
        x = c2
        y = m1 * x + c1
        if interior(line1, (x, y)) and interior(line2, (x, y)):
            rv.append((x, y))
        return rv
    
    # if line1 and line2 have the same slope
    if m1 == m2:
        if c1 != c2: #the lines don't intersect
            return rv
        # the lines have infinitely many intersection points
        # so we will return a subset of those
        lst = sorted([line1[0][0], line1[1][0], line2[0][0], line2[1][0]])
        
        i = 0
        while lst[1] + i * gap < lst[2] + gap / 2:
            x = lst[1] + i * gap
            rv.append((x, m1 * x + c1))
            i += 1
        
        return rv
    
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    if interior(line1, (x, y)) and interior(line2, (x, y)):
        rv.append((x, y))
    return rv

def checkintersect(t1start,t1end,t2start,t2end):
    return (t1start <= t2start <= t1end) or (t2start <= t1start <= t2end)

class pairs(MRJob):
    #Allows yield to be converted to .csv directly
    #OUTPUT_PROTOCOL = CsvProtocol
    #Name of loopover file, so that it doesn't have to be hardcode
    def mapper_init(self):
        directory = '0.0.csv'
        with open(directory,'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            self.spamreader = list(spamreader)

    def mapper(self, _, line):
        #directory = '/home/student/CS-123-project/FinalProject/' + os.environ['map_input_file']
        #
        for row in csv.reader([line]):
            rv = []
            #info = [pu_lon,pu_lat,do_lon,do_lat,timeblock,pu_date,do_date]
            #Implimented support for chunking
            try:
                pu_date2 = dt.datetime.strptime(row[5],'%Y-%m-%d %H:%M:%S')
                do_date2 = dt.datetime.strptime(row[6],'%Y-%m-%d %H:%M:%S')
                pu_lon2 = float(row[0])
                pu_lat2 = float(row[1])
                do_lon2 = float(row[2])
                do_lat2 = float(row[3])
            except:
                continue

            for copy in self.spamreader:
                try:
                    pu_date = dt.datetime.strptime(copy[5],'%Y-%m-%d %H:%M:%S')
                    do_date = dt.datetime.strptime(copy[6],'%Y-%m-%d %H:%M:%S')
                    pu_lon = float(copy[0])
                    pu_lat = float(copy[1])
                    do_lon = float(copy[2])
                    do_lat = float(copy[3])
                    if checkintersect(pu_date2,do_date2,pu_date,do_date):
                        rv = intersect([(pu_lon2, pu_lat2), (do_lon2, do_lat2)], [(pu_lon, pu_lat), (do_lon, do_lat)])
                        #print(round(rv[0][0],3),round(rv[0][1],3))
                        yield (round(rv[0][0],3),round(rv[0][1],3)),1
                except:
                    continue

    def combiner(self, loc, count):
        yield loc,sum(count)

    def reducer(self, loc, count):
        '''
        Defunct code: Only supports 1 reducer.

        with open('/home/student/CS-123-project/FinalProject/final.csv', "a") as csv_file:
            info = [loc[0],loc[1],loc[2],sum(count)]
            writer = csv.writer(csv_file, delimiter = ',')
            writer.writerow(info)
        '''
        yield (loc[0],loc[1]),sum(count)

    
if __name__ == '__main__':
    pairs.run()
