"""
By Harikirshna Srinivasan.
Assumptions made: * There are two lunch break, one at P-4 and other at P-5.
				    Either of which can be left out for lunch (mostly not both).
				  * Lab hour (or practical) only start at odd period and spans 2 periods continuously. (For all course with P > 0).
				  Sample Periods:
                       1            2           3           4           5           6           7           8
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
import views
import show_data
import fetch_data


def generate_timetable(db_connector: Connection,
					   cursor: Cursor, /, *,
					   campus_id: Optional[int] = None) -> None:
	# sections = fetch_data.get_sections(cursor, campus_id=campus_id)
	# classes = fetch_data.get_campuses(cursor, campus_id=campus_id)
	return None