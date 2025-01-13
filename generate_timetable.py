import random
from timetable import database

"""
By Harikirshna Srinivasan.
Assumptions made: * There are two lunch break, one at P-4 and other at P-5.
				    Either of which can be left out for lunch (mostly not both).
				  * Lab hour (or practical) only start at odd period and spans 2 periods continuously. (For all course with P > 0).
				  Sample Periods:
					   1			2			3			4			5			6			7			8
				  08:45-09:45  09:45-10:45 11:00-12:00 12:00-01:00 01:00-02:00 02:00-03:00 03:15-04:15 04:15-05:15
				  E.g., Lab hour may start at Period 5 (i.e., at 01:00) and end at 03:00
				  * For Minor Elective: No time is alloted, has to be adjusted
Considerations:  * Class capacity >= Student Strength: Allocate
				 	* Elif 2*Class capacity >= Student Strength: Allocate once again.
				 * Section has 2 diff. course / 2 diff. class in same hr, If:
				 	* Previously alloted course is elective.
					* Or, Previously alloted class is Lab & capacity < Student Strength
<<<<<<< HEAD
Limitations: 	 * Minor Specializations are left a separate time in the timetable, not allocated hr

Algorithm generate_timetable(section, *minor_elective: list[tuple[int,int]]): # day_id, period_id
	available_hrs = Fetch all days x periods
	for hr in minor_elective:
		available_hrs.remove(hr)
	odd_hrs = Odd periods from available_hrs # Assumption 2
	break_hrs = Fetch break hrs from periods # Assumption 1, Point 2
	odd_break_hr = break_hrs[0] if break_hrs[0]%2 else break_hrs[1]
	even_break_hr = break_hrs[0] if break_hrs[1]%2 else break_hrs[1]
	for day in days:
		available_hrs.remove((day, odd_break_hr))
	course_faculty_class = SELECT (course_code, faculty_id, class_id)
						   FROM faculty_teaches_class
						   JOIN section_course
						   WHERE section=section
	for crs, f_id, cls in course_faculty_class:
		capacity, cls_is_lab = Fetch capacity, is_lab from classes, where class=cls
		L, P, T, is_elective = Fetch L, P, T, is_elective from courses, where course=crs
		if cls_is_Lab:
				while P > 0:
					allocated_hr = random.choice(odd_hrs) # day, period
					while faculty_has_cls(faculty, *allocated_hr) # faculty has some class
						  or (cls_crs := fetch_cls_crs(section, *allocated_hr) # cls_crs is not-empty,
						  and (not cls_crs[0].is_lab # and cls_crs is not lab,
						  or cls in cls_crs): # and cls is already present,
						allocated_hr = random.choice(odd_hrs)

					if allocated_hr[1] in break_hrs: # if allocated_hr is break
						odd_hrs.remove((day, odd_break_hr))

					elif allocated_hr[1]+1 in break_hrs: # if allocated_hr is break
						odd_hrs.remove((day, odd_break_hr))
						available_hrs.remove((day, odd_break_hr))

					insert_into_timetable(f_id, crs, cls, *allocated_hr)
					insert_into_timetable(f_id, crs, cls, allocated_hr[0], allocated_hr[1]+1)

					available_hrs.remove((allocated_hr[0], allocated_hr[1]))
					available_hrs.remove((allocated_hr[0], allocated_hr[1]+1))

					if capacity >= (Fetch COUNT(student) From student_attends_cls WHERE cls=cls, section=section)
					   len(cls_crs) == 1:
						odd_hrs.remove((allocated_hr[0], allocated_hr[1]))
						odd_hrs.remove((allocated_hr[0], allocated_hr[1]+1))
						P -= 2
						total_hrs -= 2
		else:
			total_hrs = L+P+T
			while total_hrs:
				allocated_hr = random.choice(available_hrs)
				check = section_can_have_elective if is_elective else section_free
				while faculty_has_cls(faculty, *allocated_hr) or check(section, *allocated_hr):
					allocated_hr = random.choice(odd_hrs)
				insert_into_timetable(f_id, crs, *allocated_hr)
				if not is_elective:
					available_hrs.remove(allocated_hrs)
				total_hrs -= 1

Algorithm fetch_cls_crs(section, day, period):
	return (Fetch cls From timetable where section=section, day=day, period=period).fetchall()

Algorithm faculty_has_cls(faculty, day, period):
	return (SELECT * FROM faculty_timetable WHERE day=day, period=period).fetchone()
		   or (SELECT COUNT(*) From timeatbel where faculty=faculty, section=section, day=day)

Algorithm section_free(section, day, period):
	return not (SELECT * from timetable where section=section, day=day, period=period).fetchone()

Algorithm section_can_have_elective(section, crs, day, period):
	courses, classes = Fetch course, class from section timetable, where section=section, day=day, period=period
	return crs not in courses and all(courses.is_elective)
=======
Limitations: 	 * Minor Specialization is not considered and not left a separate time in the timetable

Algorithm generate_timetable(section):
	available_hrs = Fetch all days x periods
	odd_hrs = Odd periods from all the days # Assumption 2
	course_faculty_class = Fetch (course_code, faculty_id, class_id) from faculty_teaches_class join section_course

	for crs, f_id, cls in course_faculty_class:
		capacity, cls_is_lab = Fetch capacity, is_lab from classes, where class=cls
		L, P, T, is_elective = Fetch L, P, T, is_elective from courses, where course=crs
		total_hrs = L+P+T
		while total_hrs:
			if cls_is_Lab:
				while P > 0:
					allocated_hr = random.choice(odd_hrs)
					while faculty_has_cls(faculty, *allocated_hr) or not section_has_lab(section, cls, *allocated_hr):
						allocated_hr = random.choice(odd_hrs)

					insert_into_timetable(f_id, crs, cls, *allocated_hr)
					insert_into_timetable(f_id, crs, cls, allocated_hr[0], allocated_hr[1]+1)
					P -= 2
					total_hrs -= 2
			else:
				allocated_hr = random.choice(odd_hrs)
					while faculty_has_cls(faculty, *allocated_hr) or not section_has_elective(crs, cls, *allocated_hr):
						allocated_hr = random.choice(odd_hrs)
					
					insert_into_timetable(f_id, crs, *allocated_hr)
					total_hrs -= 1

Algorithm faculty_has_cls(faculty, day, period):
	return (SELECT * FROM faculty_timetable WHERE day=day AND period=period).fetchone()

Algorithm section_has_elective(section, course, day, period):
	courses, classes = Fetch course, class from section timetable, where section=section
	return not courses[0] or (course.is_elective and all(courses.is_elective))

Algorithm section_has_lab(section, class, day, period):
	cls_capacity, student_strength = cls_capacity_student_strength(cls, section, day, period)
	return (all(classes.is_lab) and all(cls_capacity < student_strength))

Algorithm cls_capacity_student_strength(cls, section, day, period):
	student_strength = (SELECT COUNT(*) FROM student_attends_class WHERE class=cls, section=section day=day, period=period).fetchone()
	class_capacity = (SELECT capacity FROM classes WHERE class=cls).fetchone()
	return class_capacity, student_strength
>>>>>>> 9ec0df21db46808944c299f096f1c9fdd15e3092
"""

def timetable_for(section_id):
	...

if __name__ == "__main__":
	database.close()
