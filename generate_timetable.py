"""
By Harikirshna Srinivasan.
Assumptions made: * There are two lunch break, one at P-4 and other at P-5.
					Either of which can be left out for lunch (mostly not both).
				  * Lab hour (or practical) only start at odd period and spans 2 periods continuously. (For all course with P > 0).
				  Sample Periods:
					   1			2		   3		   4		   5		   6		   7		   8
				  08:45-09:45  09:45-10:45 11:00-12:00 12:00-01:00 01:00-02:00 02:00-03:00 03:15-04:15 04:15-05:15
				  E.g., Lab hour may start at Period 5 (i.e., at 01:00) and end at 03:00
				  * First, allotted for core non-elective courses
				  * Manually, call generate timetable for Major Electives.
				  (So that can be allotted at same time for all).
				  * For Minor Electives also call the generate timetable manually.
Considerations:  * while (no_of_times_allotted)*Class capacity < Student Strength:
					* Allocate # no_of_times_allotted = 0, initially

Algorithm generate_timetable(section, *minor_elective_hrs: list[tuple[int,int]]): # day_id, period_id
	available_hrs = Fetch all days x periods
	for hr in minor_elective_hrs:
		available_hrs.remove(hr)
	odd_hrs = Odd periods from available_hrs # Assumption 2
	break_hrs = Fetch break hrs from periods # Assumption 1, Point 2
	b1, b2 = sorted(break_hrs) # needed for p-4, p-5 break check, in `lab`
	course_faculty_class = SELECT (DISTINCT course_code, faculty_id)
						   FROM faculty_teaches_class
						   INNER JOIN section_course
						   WHERE section=section
						   AND EXISTS (
								SELECT 1
								FROM courses
								WHERE code=course_code
								AND NOT is_elective
						   )
	labs = Fetch course_code, class, capacity, faculty_id, L, P, T From course_faculty_class
		   Where class.is_lab # Inner Join section_lab_class
	theories = Fetch course_code, faculty_id, L, P, T From course_faculty_class
		   Where Not class.is_lab # Inner Join section_class
	total_students = no_of_students(lab, section))
	for lab, cls, capacity, f_id, *LPT in labs:
		while LPT[1] > 0:
			allocated_hr = random.choice(odd_hrs) # day, period
			while faculty_busy_cls(f_id, *allocated_hr) # faculty has some class or attends 5 cls in day
				  or faculty_to_section(f_id, section, allocated_hr[0]) == 3 # max no. of hrs spend in same section
				  or (new_capacity := 2*(capacity-cls_occupied_by(cls, day, period))) < total_students):
				allocated_hr = random.choice(odd_hrs)

			if allocated_hr[1] == b2: # if allocated_hr is break
				odd_hrs.remove((day, b1-1)) # if allocated_hr=p-5, remove p-3 for labs
				available_hrs.remove((day, b1)) # remove p-4

			elif allocated_hr[1]+1 == b1: # if allocated_hr is break
				odd_hrs.remove((day, b2)) # if allocated_hr=p-3, remove p-5
				available_hrs.remove((day, b2)) # remove p-5

			insert_into_timetable(*allocated_hr, f_id, crs, lab)
			insert_into_timetable(allocated_hr[0], allocated_hr[1]+1, f_id, crs, lab)

			available_hrs.remove(allocated_hr)
			available_hrs.remove((allocated_hr[0], allocated_hr[1]+1))

			if new_capacity >= no_of_students:
				odd_hrs.remove((allocated_hr[0], allocated_hr[1]))
				odd_hrs.remove((allocated_hr[0], allocated_hr[1]+1))
				LPT[1] -= 2

	for lab, cls, capacity, f_id, *LPT in labs:
		total_hrs = LPT[0]+LPT[2]
		while total_hrs:
			allocated_hr = random.choice(available_hrs) # day, period
			while faculty_has_cls(f_id, *allocated_hr) # faculty has some class or attends 5 cls in day
				  or faculty_to_section(f_id, section, allocated_hr[0]) == 3 # max no. of hrs spend in same section
				  or section_busy(section, day, period): # section has some class
				allocated_hr = random.choice(available_hrs)

				insert_into_timetable(*allocated_hr, f_id, crs, cls)
				available_hrs.remove(allocated_hrs)
				total_hrs -= 1

Algorithm elective_timetable(campus_id, degree, stream, *minor_electives_code: list[str]):
	available_hrs = Fetch all days x periods Join timetable, free hr # implement algo. for <--
	electives_faculty = SELECT (DISTINCT course_code, faculty_id, L, P, T)
						FROM faculty_teaches_class # mistake - pending: bug
						INNER JOIN section_course
						WHERE section=section
						AND course_code not in minor_electives_code
						AND EXISTS (
							SELECT 1
							FROM courses
							WHERE code=course_code
							AND is_elective
						)
	for crs, f_id, *LPT in electives_faculty:
		total_hrs = sum(LPT)
		while total_hrs:
			...

Algorithm no_of_students(crs, section):
	return (SELECT COUNT(students) From section_course Join student_section where crs=crs, section=section)
				
Algorithm cls_occupied_by(cls, day, period):
	return (Fetch COUNT(student) From timetable Where cls=cls, day=day, period=period).fetchone()

Algorithm fetch_cls_crs(section, day, period): # not used now
	return (Fetch cls, crs From timetable where section=section, day=day, period=period).fetchall()

Algorithm faculty_busy_for_lab(f_id, day, period):
	faculty_hrs = (SELECT period FROM faculty_timetable As ftt
				  WHERE ftt.faculty_id=f_id, ftt.day=day,
				  ftt.period=period or ftt.period=period+1).fetchall()
	return period in faculty_hrs or len(faculty_hrs) == 5

Algorithm faculty_has_cls(f_id, day, period):
	faculty_hrs = (SELECT period FROM faculty_timetable WHERE faculty_id=f_id, day=day, period=period).fetchall()
	return period in faculty_hrs or len(faculty_hrs) == 5

Algorithm faculty_to_section(f_id, section, day):
	return (SELECT COUNT(*) FROM faculty_timetable WHERE faculty_id=f_id, section=section, day=day).fetchone()

Algorithm section_busy(section, day, period):
	return (SELECT * from timetable where section=section, day=day, period=period).fetchone()
"""
from typehints import *
import show_data
import insert_data
import fetch_data
import random
from typing import Optional, Dict, List, Tuple
import random
from typehints import Connection, Cursor

def generate_timetable(db_connector: Connection, cursor: Cursor,
                       campus_id: Optional[int] = None,
                       days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                       period_ids: List[int] = list(range(1,9)),
                       minor_elective: int = 4) -> None:
	def free_classes(day, period_id):
		cursor.execute("""SELECT `id`
					   FROM `timetables`
					   JOIN `classes`
				 	   ON `id`=`class_id`
				 	   AND NOT `is_lab`
				 	   AND `day`=%s
				 	   AND `period_id`=%s""",
					   (day, period_id))
		return {id for id in cursor.fetchall()}

	def class_capacity(class_id, day, period_id):
		cursor.execute("""SELECT `capacity`
				 	   FROM `timetables`
				 	   JOIN `classes`
				 	   ON `timetables`.`class_id`=%s
				 	   AND `id`=%s
				 	   AND `day`=%s
				 	   AND `period_id`=%s""",
					   (class_id, class_id, day, period_id))
		return cursor.fetch()["capacity"]

	def no_of_elective_students(degree, stream, elective):
		cursor.execute("""SELECT `stream`
				 	   FROM `student_electives` `SE`
				 	   JOIN `section_students` `SS`
				 	   ON `SS`.`student_id`=`SE`.`student_id`
				 	   JOIN `sections`
				 	   ON `sections`.`id`=`SS`.`section_id`
				 	   AND `campus_id`=%s
				 	   AND `degree`=%s
				 	   AND `course_code`=%s""",
					   (campus_id, degree, elective))
		return len([1 for s in cursor.fetchall() if stream is s["stream"] or stream==s["stream"]])

	section_ids = {section["id"] for section in fetch_data.get_sections(cursor, campus_id=campus_id)}

	# Allocate lab courses first
	for section_id in section_ids:
		periods = [(day, period_id)
			 for day in days for period_id in period_ids
			 if period_id % 2 == 1]
		if minor_elective:
			periods.remove(("Thursday", 7))
			periods.remove(("Friday", 7))
		faculty_course = fetch_data.get_faculty_section_courses(cursor, section_id=section_id)
		for fc in faculty_course:
			course = fetch_data.get_course(cursor, code=fc["course_code"])
			if not course["P"] or course["is_elective"]:
				continue
			hrs = course["P"]
			lab_classes = fetch_data.get_classes(cursor, campus_id=campus_id, lab=True, department=course["department"])
			while hrs:
				try:
					day, period_id, class_id = *random.choice(periods), random.choice(lab_classes)["id"]
					insert_data.add_timetable(db_connector, cursor, 
											  day=day,
											  period_id=period_id,
											  faculty_section_course_id=fc["id"],
											  class_id=class_id)
					insert_data.add_timetable(db_connector, cursor, 
											  day=day,
											  period_id=period_id+1,
											  faculty_section_course_id=fc["id"],
											  class_id=class_id)
					hrs -= 2
					periods.remove((day, period_id))
					periods.remove((day, period_id+1))
					print(section_id, day, period_id, fc, class_id)
				except Exception as e:
					print(f"Error {section_id}, {fc['faculty_id']}, {fc['id']} {fc['course_code']}: {e}")
					db_connector.rollback()
					continue
	
	# Allocate electives
	courses = fetch_data.get_courses(cursor, elective=True)
	for course in courses:
		periods = [(day, period_id)
			 for day in days for period_id in period_ids
			 if period_id % 2 == 1]
		if minor_elective:
			periods.remove(("Thursday", 7))
			periods.remove(("Thursday", 8))
			periods.remove(("Friday", 7))
			periods.remove(("Friday", 8))
		hrs = course["P"]
		lab_classes = fetch_data.get_classes(cursor, campus_id=campus_id, lab=True, department=course["department"])
		while hrs:
			try:
				day, period_id = random.choice(periods)
				if period_id % 2 == 0:
					continue
				faculty_sections = [
					fs for fs in fetch_data.get_faculty_section_courses(cursor, course_code=course["code"])
					if fs["section_id"] in section_ids
				]
				section = fetch_data.get_section(cursor, faculty_sections[0]["section_id"])
				while True:
					no_of_students = no_of_elective_students(section["degree"], section["stream"], course["code"])
					classes = set()
					for _ in range(len(faculty_sections)):
						class_id = random.choice(lab_classes)["id"]
						capacity = class_capacity(class_id, day, period_id)
						no_of_students -= capacity
						if no_of_students <= 0:
							break
					insert_data.add_timetable(db_connector, cursor, 
												day=day,
												period_id=period_id,
												faculty_section_course_id=fs["id"],
												class_id=class_id)
					insert_data.add_timetable(db_connector, cursor, 
												day=day,
												period_id=period_id+1,
												faculty_section_course_id=fs["id"],
												class_id=class_id)
					hrs -= 2
					periods.remove((day, period_id))
					periods.remove((day, period_id+1))
					print(day, period_id, fs, class_id)
					break
			except Exception as exception:
				# if exception due to lab full
				# try:
				# another lab, if not possible then allocate at some other day, period_id
				exception = exception.args
				if exception[0] != 1062:
					...
				if exception[0] == 1644:
					...
				print(f"Error {fs}: {exception}")
				db_connector.rollback()
				continue
