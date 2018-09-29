import datetime as dt
import csv
from random import randint

locs = [[75, 40], [75, 41], [74, 42]]
start = dt.datetime.strptime('2008-01-01', '%Y-%m-%d')
end = dt.datetime.strptime('2010-12-31', '%Y-%m-%d')
filename = 'testdata.csv'

date = start
rv = []
while date != end:
    for loc in locs:
        info = ['', date.strftime('%Y-%m-%d %H:%M:%S'), '','','', loc[0], loc[1]]
        cnt = randint(5, 10)
        for _ in range(cnt):
            rv.append(info)
    date += dt.timedelta(days=1)
    
with open(filename, 'w') as f:
    writer = csv.writer(f, delimiter = ',')
    for x in rv:
        writer.writerow(x)