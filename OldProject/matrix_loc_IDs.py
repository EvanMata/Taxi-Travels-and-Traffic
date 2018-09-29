from mrjob.job import MRJob
#from mr3px.csvprotocol import CsvProtocol
import re
import csv
path = "/home/eamata/CS-123-project/t1"

#Evan Mata

#Use the following command to make a first.csv file of the first few 
#lines of data.
#head -n 5000 yellow_tripdata_2016-08.csv >> first.csv

#Use the following command to find the max lat/lon of my data set w/o opening it
#awk '{if(max<$1){max=$8;line=$8}}END{print line}' file 
#start lat, lon, end lat, lon are cols 7, 8, 11, 12 respectively. 

class matrix(MRJob):

	#OUTPUT_PROTOCOL = CsvProtocol #Should allow me to write the output as a csv.

	def mapper(self, _, line):
		
		line_info = [0]*17 #We have 18 lines of data.
		line_orig_info = line.split(',') #csv so delimter is ,
		if len(line_orig_info) > 17:
			for i in range(1, 17):
				#Possibly eliminate exception cases.
				line_info[i - 1] = line_orig_info[i] 
			line_info[0] = line_orig_info[0] + line_orig_info[1]
		else:
			line_info = line_orig_info

		(vendorID, pickup_time, dropoff_time, passenger_count, trip_dist, \
		rate_code, store_and_forward, PU_loc_id, DO_loc_id, \
		payment_type, fare_amt, extra, mta_tax, tip_amt, tolls_amt, \
		improvement_surcharge, total_amt) = line_info

		dates = re.findall(r'\d{2}-\d{2}-\d{2}', pickup_time)
		
		for date in dates:
			yield date + ' ' + PU_loc_id, 1
		
		#yield PU_loc_id, 1

	def combiner(self, loc, counts):
		yield loc, sum(counts)

	def reducer(self, loc, counts):
		#Here we will want to sum them, then put them into a matrix.
		with open(path, "a") as csv_file:
			counts_list = list(counts)
			info = [loc, sum(counts_list)]
			writer = csv.writer(csv_file, delimiter = ',')
			writer.writerow(info)
		#yield loc, sum(counts)

if __name__ == '__main__':
	matrix.run()