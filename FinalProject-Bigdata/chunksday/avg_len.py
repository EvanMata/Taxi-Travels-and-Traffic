import csv
import datetime as dt

file_info = '0.0.csv'

#Calculate the average length of time for a taxi trip.
def avg_len(input_file):
	with open(input_file) as csvfile:
		count = 0.0
		total_time = 0.0
		spamreader = csv.reader(csvfile, delimiter=',')
		for copy in spamreader:
			try:
				pu_date = dt.datetime.strptime(copy[5],'%Y-%m-%d %H:%M:%S')
				do_date = dt.datetime.strptime(copy[6],'%Y-%m-%d %H:%M:%S')
				trip_len = abs(pu_date - do_date)
				info = divmod(trip_len.total_seconds(), 60)
				minutes = info[0]
				count += 1
				total_time += minutes
			except:
				pass
		return total_time/count


if __name__ == "__main__":
	avg_trip_len = avg_len(file_info)
	print(avg_trip_len)