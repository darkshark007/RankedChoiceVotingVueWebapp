import time
import math

class Progress():
	
	def __init__(self, total):
		self.total = total
		self.start = int(round(time.time() * 1000))

	def get_progress_string(self, current, show_time=False):
		current_percent = math.floor(current*10000.0/self.total)/100.0
		
		time_since_start = int(round(time.time() * 1000))-self.start
		if current_percent == 0:
			estimated_total_time = 0
		else:
			estimated_total_time = (time_since_start / (current_percent/100.0))
		estimated_time_remaining = math.floor(estimated_total_time-time_since_start)
		
		# Generate the Percent String
		percent_string = "%s" % (current_percent)
		# Set 2 decimal places
		try:
			num_places = len(percent_string)-percent_string.index(".")-1
			percent_string = percent_string + "0"*(2-num_places)
		except ValueError:
			percent_string = percent_string+".00"
		# Add Trim
		percent_string = "(%s%s)" % (percent_string, "%")
		# Pad it
		while len(percent_string) < 9:
			percent_string = " "+percent_string
		if show_time:
			progress_string = 'Progress: %s/%s %s %s seconds remaining' % (current, self.total, percent_string, math.floor(estimated_time_remaining/1000.0))
		else:
			progress_string = 'Progress: %s/%s %s' % (current, self.total, percent_string)
		
		context = {
			'progress_string': progress_string,
			'percent_string': percent_string,
			'estimated_time_remaining': estimated_time_remaining,
			'current_percent': current_percent,			
		}
		
		return context
	
		
	def set_total(self, new_total):
		self.total = new_total
	
	
	@staticmethod
	def _test(total=15000000):
		p = Progress(total)
		for idx in range(0,total):
			# Python 2
			# print("%s %s" % (p.get_progress_string(idx), "\b"*150)),
			# Python 3
			print("%s %s" % (p.get_progress_string(idx)['progress_string'], "\b"*150), end='')
		print("%s" % ("\b"*150))
