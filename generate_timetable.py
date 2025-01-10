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
"""

def timetable_for(section_id):
	...

if __name__ == "__main__":
	database.close()
