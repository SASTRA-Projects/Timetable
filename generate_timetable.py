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
					* no_of_times_allotted = 0, initially
"""
from typehints import *
import show_data
import insert_data
import fetch_data
import delete_data
import random
from typing import *
import random
from itertools import combinations
from functools import reduce
from typehints import Connection, Cursor

def generate_timetable(db_connector: Connection, cursor: Cursor,
                       campus_id: Optional[int] = None,
                       days: Tuple[str] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
                       period_ids: Tuple[int] = tuple(range(1,9)),
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

	def max_lab_capacity(department, day, period_id):
		cursor.execute("""SELECT COUNT(*) / `P` AS `labs_per_week`,
				 	   `section_id`, `degree`, `stream`, `course_code`
				 	   FROM `timetables`
				 	   JOIN `faculty_section_course` `FSC`
				 	   ON `FSC`.`id`=`faculty_section_course_id`
				 	   JOIN `courses`
				 	   ON `course_code`=`code`
					   JOIN `classes`
				 	   ON `classes`.`id`=`class_id`
				 	   AND `is_lab`
				 	   JOIN `sections`
				 	   ON `sections`.`id`=`section_id`
				 	   AND `campus_id`=%s
				 	   AND `classes`.`department`=%s
				 	   GROUP BY `section_id`, `course_code`""",
					   (campus_id, department))
		sec_crs = cursor.fetchall()
		cursor.execute("""SELECT COUNT(*) AS `no_of_students`,
				 	   `FSC`.`section_id`, `course_code`
				 	   FROM `faculty_section_course` `FSC`
				 	   JOIN `courses`
				 	   ON `course_code`=`code`
				 	   AND NOT `is_elective`
				 	   JOIN `sections`
				 	   ON `sections`.`id`=`FSC`.`section_id`
				 	   JOIN `section_students` `SS`
				 	   ON `SS`.`section_id`=`sections`.`id`
				 	   AND `campus_id`=%s
				 	   AND `courses`.`department`=%s
				 	   GROUP BY `FSC`.`section_id`, `code`""",
					   (campus_id, department))
		no_of_students = cursor.fetchall()
		cursor.execute("""SELECT COUNT(*) AS `no_of_sections`,
				 	   `course_code`, `degree`, `stream`
				 	   FROM `faculty_section_course` `FSC`
				 	   JOIN `sections`
				 	   ON `sections`.`id`=`FSC`.`section_id`
				 	   JOIN `courses`
				 	   ON `code`=`course_code`
				 	   AND `campus_id`=%s
				 	   AND `department`=%s
				 	   AND `is_elective`
				 	   AND `P`
				 	   GROUP BY `code`, `degree`, `stream`""",
					   (campus_id, department))
		no_of_sections = cursor.fetchall()
		cursor.execute("""SELECT COUNT(*) AS `no_of_students`,
				 	   `course_code`, `degree`, `stream`
					   FROM `section_students` `SS`
				 	   JOIN `sections`
				 	   ON `SS`.`section_id`=`sections`.`id`
				 	   JOIN `student_electives` `SE`
					   ON `SS`.`student_id`=`SE`.`student_id`
					   JOIN `courses`
					   ON `course_code`=`code`
				 	   AND `is_elective`
				 	   AND `P`
				 	   AND `campus_id`=%s
				 	   AND `department`=%s
				 	   GROUP BY `code`, `degree`, `stream`""",
					   (campus_id, department))
		no_of_elective_students = cursor.fetchall()
		cursor.execute("""SELECT `class_id`, `capacity`, `section_id`,
				 	   `course_code`, `degree`, `stream`, `is_elective`
				 	   FROM `timetables`
					   JOIN `faculty_section_course` `FSC`
				 	   ON `FSC`.`id`=`faculty_section_course_id`
				 	   JOIN `classes`
				 	   ON `classes`.`id`=`class_id`
				 	   AND `is_lab`
				 	   AND `day`=%s
				 	   AND `period_id`=%s
				 	   JOIN `courses`
				 	   ON `course_code`=`code`
				 	   JOIN `sections`
				 	   ON `section_id`=`sections`.`id`
				 	   AND `campus_id`=%s
				 	   AND `courses`.`department`=%s""",
					   (day, period_id, campus_id, department))
		class_capacity = list(cursor.fetchall())
		cursor.execute("""SELECT `classes`.`id` AS `class_id`, `capacity`
				 	   FROM `classes`
				 	   JOIN `campus_buildings` `CB`
				 	   ON `CB`.`building_id`=`classes`.`building_id`
				 	   AND `is_lab`
				 	   AND `campus_id`=%s
				 	   AND `department`=%s""", ( campus_id, department))
		classes = cursor.fetchall()
		elective_std_sec = {(std["degree"], std["stream"], std["course_code"]): std["no_of_students"] // sec["no_of_sections"]
					  		for std in no_of_elective_students
							for sec in no_of_sections
							if std["degree"] == sec["degree"]
							and std["stream"] == sec["stream"]
							and std["course_code"] == sec["course_code"]}
		cls_sec_crs = {(sc["course_code"], sc["section_id"]): sc["labs_per_week"]
				 	   for cls in class_capacity
					   for sc in sec_crs
					   if sc["course_code"] == cls["course_code"]
					   and sc["section_id"] == cls["section_id"]}
		std_sec = {(std["section_id"], std["course_code"]): std["no_of_students"]
			 	   for std in no_of_students
				   for cls in class_capacity
				   if std["course_code"] == cls["course_code"]
				   and std["section_id"] == cls["section_id"]}
		for cls in class_capacity:
			if cls["is_elective"]:
				cls["capacity"] -= elective_std_sec[(cls["degree"], cls["stream"], cls["course_code"])] // cls_sec_crs[(cls["course_code"], cls["section_id"])]
			else:
				cls["capacity"] -= std_sec[(cls["section_id"], cls["course_code"])] // cls_sec_crs[(cls["course_code"], cls["section_id"])]

		for cls in classes:
			if not any(cls["class_id"] == c["class_id"] for c in class_capacity):
				class_capacity.append(cls)

		class_capacity = sorted(list({(cls["class_id"], int(cls["capacity"])) for cls in class_capacity}), key=lambda x: x[1], reverse=True)
		return [[*cls] for cls in class_capacity]

	def is_faculty_free(faculty_id, day, period):
		cursor.execute("""SELECT 1
				 	   FROM `timetables`
				 	   JOIN `faculty_section_course` `FSC`
				 	   ON `FSC`.`id`=`faculty_section_course_id`
				 	   AND `faculty_id`=%s
				 	   AND `day`=%s
				 	   AND `period_id`=%s
				 	   LIMIT 1""", (faculty_id, day, period_id))
		return not cursor.fetchone()

	def sorted_and_reverse(courses=None, no_of_electives=None, combs=[]):
		rev = lambda combs: sorted(combs | {c for comb in combs if (c := comb[::-1]) and c not in combs}, key=lambda x: (-len(x), x))
		if combs:
			return rev(set(combs))
		else:
			combs = {comb for i in range(1, no_of_electives+1) for comb in combinations(courses, i)}
			combs = {comb  if len(comb) > 1 else (comb[0], comb[0]) for comb in combs}
			return rev(combs)

	def transitive(allowed, c1, c2):
		c3 = (c1[0], c2[-1])
		for c in allowed:
			if c == c3:
				return tuple({*c1, *c2, *c3})
		else:
			return None

	def try_compress(section_id):
		cursor.execute("""SELECT `day`, `period_id`, `faculty_section_course_id`, `class_id`
				 	   FROM `timetables`
				 	   JOIN `faculty_section_course`
					   ON `id`=`faculty_section_course_id`
				 	   AND `section_id`=%s
				 	   ORDER BY `day`, `period_id`""", (section_id,))
		timetable = cursor.fetchall()
		... # TODO

	programmes = show_data.get_programmes(cursor, campus_id=campus_id)
	sections = fetch_data.get_sections(cursor, campus_id=campus_id)
	section_ids = {section["id"] for section in sections}
	student_electives = fetch_data.get_student_electives(cursor)

	# 1. Allocate elective labs: Assume no elective if stream is None
	for programme in programmes:
		courses = fetch_data.get_courses(cursor, programme_id=programme["id"], elective=True)
		_sections =  [section for section in sections if section["degree"]==programme["degree"]]
		for year in range(show_data.get_degree_duration(cursor, degree=programme["degree"])):
			_section_ids = {section["id"] for section in _sections if section["year"]==year}
			_student_ids = {student["student_id"] for section_id in _section_ids
							for student in fetch_data.get_section_students(cursor, section_id=section_id)}
			_student_electives = {course["code"]: student_ids for course in courses
						 		  if (student_ids := {se["student_id"] for se in student_electives
							   						  if se["course_code"] == course["code"] and se["student_id"] in _student_ids})}
			if not _student_electives:
				continue
			_courses = set(_student_electives.keys())
			no_of_electives = 0
			student_id = tuple(_student_electives[tuple(_courses)[0]])[0]
			for course, student_ids in _student_electives.items():
				if student_id in student_ids:
					no_of_electives += 1

			if no_of_electives > 1:
				allowed = set(sorted_and_reverse(courses=_courses, no_of_electives=no_of_electives))
				not_allowed = set()
				students = set()
				for se1 in student_electives:
					for student_id in se1[1]:
						if student_id in students:
							continue
						else:
							students.add(student_id)
						num = 0
						electives = set()
						for se2 in student_electives:
							if student_id in se2[1]:
								num += 1
								electives.add(se2["course_code"])
								if num == no_of_electives:
									break
						electives = tuple(sorted(electives))
						not_allowed.add(electives)
						not_allowed.add(electives[::-1])

				allowed -= not_allowed
				allowed = sorted_and_reverse(combs=allowed)
				for c1 in allowed:
					for c2 in allowed:
						if c1 != c2 and c1[-1] == c2[0]:
							allowed.remove(c1)
							allowed.remove(c2)
							course = transitive(allowed, c1, c2)
							if not course:
								allowed.append(c1)
								allowed.append(c2)
							else:
								allowed.append(course)
								course = course[::-1]
								if course not in allowed:
									allowed.append(course)
								break

				allowed = [set(course) for course in allowed]
				for course in allowed:
					allowed.remove(course)
					if course not in allowed:
						allowed.insert(0, course)

				allowed = sorted((tuple(sorted(course)) for course in allowed), key=lambda x: (-len(x), x))
				over = set()
				not_allowed = set()
				for course in allowed:
					if all(c in over for c in course):
						not_allowed.add(course)
					elif not any(c in over for c in course):
						over |= set(course)
					else:
						for c2 in course:
							if c2 not in over:
								if (c2,) == course:
									break # not deleting it
								elif (c2,) not in allowed:
									allowed.append((c2,))
						else:
							not_allowed.add(course)

				assert course != over, "Unable to allot for all the electives"
				for course in not_allowed:
					allowed.remove(course)

			else:
				allowed = [tuple(_courses)]

			assert len(allowed) <= no_of_electives+1, f"Cannot allocate efficiently within {no_of_electives+1} periods"
			periods = {(day, period_id) for day in days for period_id in period_ids}
			if minor_elective:
				periods.remove(("Thursday", 7))
				periods.remove(("Thursday", 8))
				periods.remove(("Friday", 7))
				periods.remove(("Friday", 8))
			# TODO
			print(allowed)

	# 2. Allocate lab courses
	for section_id in section_ids:
		periods = {(day, period_id)
				   for day in days[::-1]
				   for period_id in period_ids
				   if period_id % 2 == 1}
		if minor_elective:
			periods.remove(("Thursday", 7))
			periods.remove(("Friday", 7))
		no_of_students = len(fetch_data.get_section_students(cursor, section_id=section_id))
		cls = fetch_data.get_classes(cursor, section_id=section_id)[0]
		faculty_courses = fetch_data.get_faculty_section_courses(cursor, section_id=section_id)
		twice = []
		ctwice = False
		for fc in faculty_courses:
			course = fetch_data.get_lab_departments(cursor, course_code=fc["course_code"], elective=False)
			if not course:
				continue
			course = course[0]
			hrs = course["P"]
			lab_departments = course["lab_departments"]
			no_of_labs = len(lab_departments)
			assert no_of_labs == 1 or 2 * no_of_labs == hrs, "Number of lab-departments does not match with practical hours"

			labs = []
			for ld in lab_departments:
				class_day_period = []
				for period in periods:
					if ld == "":
						class_day_period.append((([cls["id"], cls["capacity"]],), period))
						continue
					class_day_period.append((max_lab_capacity(ld, *period), period))
				assert class_day_period, "No lab is available..."
				labs.append(class_day_period)

			if no_of_labs == 1:
				labs *= (hrs // 2)

			while hrs:
				try:
					no_of_times = 1
					class_day_period = sorted(labs[-1], key=lambda x: x[0][0][1], reverse=True)
					while class_day_period[0][1] not in periods:
						class_day_period.pop(0)
					class_id, capacity = class_day_period[0][0][0]
					day, period_id = class_day_period[0][1]
					if capacity < no_of_students // no_of_times:
						if ctwice:
							for cdp in class_day_period:
								if cdp[1] == twice[0]:
									class_id, capacity = cdp[0][0]
									day, period_id = twice[0]
									break
						no_of_times = 2

					if capacity < no_of_students // no_of_times or not class_day_period:
						if not ctwice:
							print("Too many students & too less capacity in all the labs...", class_day_period, capacity, no_of_students)
						else:
							ctwice = False # Lab is too busy at this time...
							continue
						return None
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
					class_day_period[0][0][0][1] -= no_of_students // no_of_times
					prev_day = day
					if no_of_times-1:
						if not ctwice:
							ctwice = True
							twice.append((day, period_id))
							while class_day_period[1][1] not in periods or class_day_period[1][1][0] == prev_day:
								class_day_period.pop(1)
							class_id, capacity = class_day_period[1][0][0]
							day, period_id = class_day_period[1][1]
						else:
							periods.remove((day, period_id))
							for cdp in class_day_period:
								if cdp[1] == twice[1]:
									class_id, capacity = cdp[0][0]
									day, period_id = twice[1]
									break
							twice.clear()
							ctwice = False
						if capacity < no_of_students // 2:
							print("Too many students & too less capacity in all the labs...", class_day_period, capacity, no_of_students)
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
						class_day_period[1][0][0][1] -= no_of_students // no_of_times
						if ctwice:
							twice.append((day, period_id))
							ctwice = True
					if not ctwice:
						periods.remove((day, period_id))
					ctwice = True if twice else False
					hrs -= 2
					labs.pop()
					print(section_id, day, period_id, fc, class_id)
					db_connector.commit()
				except Exception as exception:
					exception = exception.args
					delete_data.delete_timetable(db_connector, cursor,
												day=day, period_id=period_id, faculty_section_course_id=fc["id"], class_id=class_id)
					delete_data.delete_timetable(db_connector, cursor,
												day=day, period_id=period_id+1, faculty_section_course_id=fc["id"], class_id=class_id)
					if exception[1] == "Same faculty cannot take more than 3 class for the same section on the same day":
						for cdp in class_day_period:
							if cdp[1][0] == day:
								labs[-1].remove(cdp)
						ctwice = False
					elif exception[1] == "Same faculty cannot take more than one class at the same time":
						for cdp in class_day_period:
							if cdp[1] == (day, period_id):
								labs[-1].remove(cdp)
								break
					elif exception[1] == "Invalid Schedule: This hour is supposed for lunch":
						for cdp in class_day_period:
							if cdp[1] == (day, period_id):
								labs[-1].remove(cdp)
								break
						periods.remove((day, period_id))
					elif exception == ("list index out of range",):
						return None
					print(f"Error {section_id} {day}{period_id} {fc["faculty_id"]}, {fc["id"]} {fc["course_code"]}: {exception}{no_of_students}")
					continue

	# 3. Allocate non-elective, non-lab hrs
	for section in sections[::-1]:
		period_ids = (1, 2, 3, 4, 6, 7, 8)
		period_ids_weights = (6, 8, 11, 11, 11, 6, 4)
		days_weights = 5 * (1,)
		periods = [(day, period_id) for period_id in period_ids for day in days]
		periods_weights = [day_w * period_w for period_w in period_ids_weights for day_w in days_weights]
		if minor_elective:
			idx = periods.index(("Thursday", 7))
			periods_weights.pop(idx)
			periods.pop(idx)
			idx = periods.index(("Thursday", 8))
			periods_weights.pop(idx)
			periods.pop(idx)
			idx = periods.index(("Friday", 7))
			periods_weights.pop(idx)
			periods.pop(idx)
			idx = periods.index(("Friday", 8))
			periods_weights.pop(idx)
			periods.pop(idx)

		faculty_courses = fetch_data.get_faculty_section_courses(cursor, section_id=section["id"])
		class_id = fetch_data.get_section_classes(cursor, section_id=section["id"])[0]["class_id"]
		print(section)
		for fc in faculty_courses:
			course = fetch_data.get_course(cursor, code=fc["course_code"])
			if not course or course["is_elective"]:
				continue
			hrs = course["L"] + course["T"]
			while hrs:
				try:
					day, period_id = random.choices(periods, weights=periods_weights)[0]
					insert_data.add_timetable(db_connector, cursor,
											  day=day,
											  period_id=period_id,
											  faculty_section_course_id=fc["id"],
											  class_id=class_id)
					hrs -= 1
					idx = periods.index((day, period_id))
					periods_weights.pop(idx)
					periods.pop(idx)
					db_connector.commit()
				except Exception as exception:
					exception = exception.args
					delete_data.delete_timetable(db_connector, cursor,
												day=day, period_id=period_id, faculty_section_course_id=fc["id"], class_id=class_id)
					if exception[0] == 1644 and exception[1].find("Same faculty") == -1:
						idx = periods.index((day, period_id))
						periods_weights.pop(idx)
						periods.pop(idx)
						print(periods_weights, len(periods))
					elif exception == ("list index out of range",):
						print("list index out of range")
						return None
					print(f"Error {section["id"]},{day}{period_id} {fc["faculty_id"]}, {fc["id"]} {fc["course_code"]}: {exception}")
					continue
