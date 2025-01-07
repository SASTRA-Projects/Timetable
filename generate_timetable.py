import random
from timetable import database

"""available slots are fetched
fetch breaks
for subject taught in class:
	fetch faculty
	while total_periods:
		pure_random(day)
		fetch day's timetable that are free, if empty period = random(period < 1st break) insert tot--
											 else last period + 1 insert tot--, if not available then continue
"""
def timetable_for(class_id):
	...

if __name__ == "__main__":
	database.close()
