import pandas as pd
from mrjob.job import MRJob
import csv
import re
from shapely.geometry import Point, Polygon, shape
import json

filename = 'tract.json'
polys = []


if filename:
    with open(filename, 'r') as f:
        js = json.load(f)
for feature in js['features']:
    #print(feature)
    poly = (shape(feature['geometry']),feature['properties']['namelsad'])
    polys.append(poly)

def gentest():
    df = pd.read_csv("firstnypd.csv")
    df = df[["Latitude","Longitude"]]
    df.dropna(inplace=True)
    df.to_csv('latlong.csv')

def check(lat,longi):
    '''
    Check which community area belongs to which community area. This is using
    Shapely to check whether a point belongs in a multipolygon.

    Inputs : Lat, Longitude
    Output : Community area which the Lat, Long belongs to
    '''

    # construct point based on lon/lat returned by geocoder
    point = Point(longi,lat)

    # check each polygon to see if it contains the point
    for poly in polys:
        if poly[0].contains(point):
            return poly[1]


class main(MRJob):
    def mapper(self, _, line): 
        for row in csv.reader([line]):
            try:
                fl0 = float(row[0])
                fl1 = float(row[1])
                fl2 = float(row[2])
                fl3 = float(row[3])
                #print(fl0,fl1)
            except (ValueError):
                fl0 = None
            if fl0 != None:
                tract = check(fl1,fl0)
                #print((tract,fl2), fl3)
                yield (tract,fl2), fl3

    def combiner(self, tract, counts):
        yield tract, sum(counts)

    def reducer(self, tract, counts):
        with open('/home/student/CS-123-project/FinalProject/heatmap.csv', "a") as csv_file:
            counts_list = list(counts)
            info = [tract[0],tract[1], sum(counts_list)]
            writer = csv.writer(csv_file, delimiter = ',')
            writer.writerow(info)
        #yield tract, sum(counts)

if __name__ == '__main__':
    main.run()
