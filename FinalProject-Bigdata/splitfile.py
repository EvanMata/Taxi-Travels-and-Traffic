import datetime as dt
import csv


start = dt.datetime(2018,1,1,0,0)
date_list = [(start + dt.timedelta(hours=2*x)).time() for x in range(0, 12)]

def timeblocksslow(t2start,t2end):
    '''We are not using this code anymore since it is slow and a roundabout way
    of determining which chunk time falls in'''
    
    t2start = t2start.time()
    for i,v in enumerate(date_list):
        t1start = v
        if i+1 == len(date_list):
            t1end = dt.datetime(23,59,59)
        else:
            t1end = date_list[i+1]

        if (t2start <= t1end):
            return i

def timeblocks(tstart,tend):
    tstart = tstart.hour
    return tstart//1.5

def run(time=False,day=False):
    i = 0
    if day == False:
        end_date = dt.datetime(2016,1,7,23,59,59)
        path = './chunksweek/'
    else:
        end_date = dt.datetime(2016,1,1,23,59,59)
        path = './chunksday/'
    with open('yellow_tripdata_2016-01.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for copy in spamreader:
            try:
                pu_date = dt.datetime.strptime(copy[1],'%Y-%m-%d %H:%M:%S')
                do_date = dt.datetime.strptime(copy[2],'%Y-%m-%d %H:%M:%S')
                pu_lon = float(copy[5])
                pu_lat = float(copy[6])
                do_lon = float(copy[9])
                do_lat = float(copy[10])

                if time == True:
                    if pu_date <= end_date:
                        timeblock = timeblocks(pu_date,do_date)
                        filename = path + str(timeblock) + '.csv'

                        info = [pu_lon,pu_lat,do_lon,do_lat,timeblock,pu_date,do_date]
                        with open(filename, "a") as csv_file:
                            writer = csv.writer(csv_file, delimiter = ',')
                            writer.writerow(info)
                else:
                    timeblock = timeblocks(pu_date,do_date)
                    filename = './chunks/' + str(timeblock) + '.csv'

                    info = [pu_lon,pu_lat,do_lon,do_lat,timeblock,pu_date,do_date]
                    with open(filename, "a") as csv_file:
                        writer = csv.writer(csv_file, delimiter = ',')
                        writer.writerow(info)
                i+=1
            except:
                pass

            if(i%100000==0):
                print(i)
