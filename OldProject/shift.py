from mrjob.job import MRJob
import datetime as dt

shift_vals = range(1, 31)
start_date = dt.datetime.strptime('2009-01-01', '%Y-%m-%d')
end_date = dt.datetime.strptime('2009-12-31', '%Y-%m-%d')

class shift(MRJob):
	def mapper(self, _, line):
		lst = line.split(',')
		pu_date = dt.datetime.strptime(lst[1],'%Y-%m-%d %H:%M:%S')
		pu_lon = round(float(lst[5]), 4)
		pu_lat = round(float(lst[6]), 4)
		pu_ad = str(pu_lon) + ' ' + str(pu_lat)
		yield pu_ad, pu_date.strftime('%Y-%m-%d')

	def combiner(self, pu_ad, pu_date):
		rv = {}
		for date in pu_date:
			rv[date] = rv.get(date, 0) + 1
		for date, cnt in rv.items():
			yield pu_ad, [date, cnt]

	def reducer(self, pu_ad, date_cnt):
		rv = {}
		for x in date_cnt:
			date = x[0]
			cnt = x[1]
			rv[date] = rv.get(date, 0) + cnt
		# we can possibly write rv to a csv file at this point

		date = start_date
		sum_sq_lst = []
		for s in shift_vals:
			sum_sq = 0
			while date != end_date:
				shifted = date + dt.timedelta(days=s)
				sum_sq += (rv[date.strftime('%Y-%m-%d')] - rv[shifted.strftime('%Y-%m-%d')])**2
				date += dt.timedelta(days=1)
			sum_sq_lst.append([s, sum_sq])
			date = start_date

		for y in sum_sq_lst:
			yield pu_ad, y

if __name__ == '__main__':
	shift.run()