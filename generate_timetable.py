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
import random
import heapq


def generate_timetable(db_connector: Connection,
					   cursor: Cursor, /, *,
					   campus_id: Optional[int] = None) -> None:
	# sections = fetch_data.get_sections(cursor, campus_id=campus_id)
	# classes = fetch_data.get_campuses(cursor, campus_id=campus_id)
	return None

def generate_timetable(db_connector: Connection,
					   cursor: Cursor, /, *,
					   campus_id: Optional[int] = None,
					   days: int = 5,
					   periods: int = 8,
					   minor_elective: bool = True,
					   minor_hrs: Dict[int, Set[int, int]] = {4: {7, 8}, 5: {7, 8}}) -> None:
    """
    Generate a timetable for a campus. This function assumes that helper functions,
    such as get_courses, get_section, etc., are predefined in your module.
    It also uses try/except to backtrace in case of a collision or insertion error.
    """

    # Define available hours (days: 1-5, periods: 1-8)
    available_hrs: Dict[int, Set[int]] = {
		day_i: {period_i for period_i in range(1, periods+1)}
		for day_i in range(1, days+1)
	}

    # Remove hours already allocated for minor electives (if any)
    # For example, assume minor_elective_hrs is fetched from the db or passed in.
	if minor_elective:
		if not minor_hrs:
			raise TypeError("Minor Elective should have non-empty Day(s): Period(s)")
    for (day, periods) in minor_elective_hrs.items():
		if day in available_hrs:
			available_hrs[day] -= periods

    # Identify odd periods for lab scheduling (lab hours must start on odd periods)
    odd_hrs: Dict[int, Set[int]] = {
		day: period for (day, period) in available_hrs.items()
		if period % 2 == 1
	}

    # Define break periods (assumption: periods 4 and 5 are lunch breaks)
    break_periods: Set[int] = {4, 5}
    b1: int, b2: int = sorted(break_periods)

    # Fetch core (non-elective) courses with their faculty and class IDs for the given campus
    cursor.execute("""SELECT DISTINCT(`course_code`), `faculty_id`, `section_id` 
                   FROM `faculty_section_course` `FTC`
                   JOIN `sections`
                   ON `FTC`.`section_id`=`sections`.`id`
                   AND `sections`.`campus_id`=%s""", (campus_id,))
    course_faculty_section = cursor.fetchall()

    # Separate lab courses and theory classes (using get_section to check if a class is a lab)
#     labs = [(course, class_id, faculty_id) 
#             for course, faculty_id, class_id in course_faculty_class
#             if class_id and get_section(cursor, id=class_id)["is_lab"]]
#     theories = [(course, faculty_id, class_id) 
#                 for course, faculty_id, class_id in course_faculty_class
#                 if not class_id or not get_section(cursor, id=class_id)["is_lab"]]

#     # Assume each section has a field "num_students"
#     # For demonstration, choose the first section from sections for the campus
#     section = cursor.execute("SELECT id, num_students FROM sections WHERE campus_id = ? LIMIT 1", (campus_id,)).fetchone()
#     if not section:
#         print("No section found for campus_id", campus_id)
#         return
#     section_id, total_students = section

#     # Track faculty and section usage: dicts with day as key and usage count as value
#     faculty_usage = {}  # {faculty_id: {day: usage_count}}
#     section_usage = {day: 0 for day in range(5)}

#     # Initialize usage for each faculty in our course_faculty_class list
#     for _, faculty_id, _ in course_faculty_class:
#         if faculty_id not in faculty_usage:
#             faculty_usage[faculty_id] = {day: 0 for day in range(5)}

#     # Helper function to attempt an insertion into the timetable with backtracing.
#     def safe_insert(day: int, period: int, faculty_id: int, course_code: str, class_id: Optional[int]) -> bool:
#         try:
#             insert_into_timetable(cursor, day, period, faculty_id, course_code, class_id)
#             db_connector.commit()
#             return True
#         except Exception as e:
#             # On collision or other insertion errors, roll back the change and return False.
#             db_connector.rollback()
#             print(f"Insertion failed at day {day}, period {period} for course {course_code}: {e}")
#             return False

#     # ALLOCATE LAB HOURS
#     for course_code, class_id, faculty_id in labs:
#         # For demonstration, assume each lab must be scheduled for 2 periods continuously
#         lab_capacity = get_section(cursor, id=class_id)["capacity"]
#         remaining_students = total_students  # initial remaining students

#         # Continue scheduling lab sessions until capacity requirement met
#         while remaining_students > 0:
#             allocated_hr = random.choice(odd_hrs)  # Pick a random odd period
#             day, period = allocated_hr

#             # Check constraints: max 5 hrs per faculty per day, section not overloaded, etc.
#             if faculty_usage[faculty_id][day] >= 5 or section_usage[day] >= 8:
#                 continue
#             # Example capacity check, you can replace with your actual function:
#             if 2 * (lab_capacity - class_occupied_by(cursor, class_id, day, period)) < remaining_students:
#                 continue

#             # Check for break collision: if lab starts at a break period, adjust available hours
#             if period == b2:
#                 if (day, b1 - 1) in odd_hrs:
#                     odd_hrs.remove((day, b1 - 1))
#                 if (day, b1) in available_hrs:
#                     available_hrs.remove((day, b1))
#             elif period + 1 == b1:
#                 if (day, b2) in odd_hrs:
#                     odd_hrs.remove((day, b2))
#                 if (day, b2) in available_hrs:
#                     available_hrs.remove((day, b2))
            
#             # Try to insert for both periods (lab spans 2 continuous periods)
#             success_first = safe_insert(day, period, faculty_id, course_code, class_id)
#             success_second = safe_insert(day, period + 1, faculty_id, course_code, class_id)
#             if success_first and success_second:
#                 # Update usage stats
#                 faculty_usage[faculty_id][day] += 2
#                 section_usage[day] += 2
#                 # Remove the allocated hours from available lists
#                 if allocated_hr in available_hrs:
#                     available_hrs.remove(allocated_hr)
#                 if (day, period + 1) in available_hrs:
#                     available_hrs.remove((day, period + 1))
#                 remaining_students -= 2 * lab_capacity
#             else:
#                 # If insertion fails, try a different slot by continuing the loop
#                 continue

#     # ALLOCATE THEORY HOURS
#     for course_code, faculty_id, class_id in theories:
#         # Get theory hours from course info (e.g., lecture + tutorial hours)
#         course_info = get_courses(cursor, id=course_code)
#         total_hrs = course_info.get("L", 0) + course_info.get("T", 0)

#         while total_hrs > 0:
#             allocated_hr = random.choice(available_hrs)
#             day, period = allocated_hr

#             # Check constraints for faculty and section
#             if faculty_usage[faculty_id][day] >= 5 or section_usage[day] >= 8:
#                 continue
#             if section_busy(cursor, section_id, day, period):
#                 continue

#             # Try to insert into timetable; if insertion fails, backtrace and pick another slot
#             if safe_insert(day, period, faculty_id, course_code, class_id):
#                 faculty_usage[faculty_id][day] += 1
#                 section_usage[day] += 1
#                 total_hrs -= 1
#                 available_hrs.remove(allocated_hr)
#             else:
#                 continue

#     print("Timetable generation complete.")

# # Predefined helper functions (stubs for demonstration)

# def insert_into_timetable(cursor: Cursor, day: int, period: int, faculty_id: int,
#                             course_code: str, class_id: Optional[int]) -> None:
#     """
#     Insert a class into the timetable table.
#     This is a stub function; replace with your actual database insertion logic.
#     """
#     cursor.execute("""
#         INSERT INTO timetable (day, period, faculty_id, course_code, class_id)
#         VALUES (?, ?, ?, ?, ?)
#     """, (day, period, faculty_id, course_code, class_id))

# def class_occupied_by(cursor: Cursor, class_id: int, day: int, period: int) -> int:
#     """
#     Returns the number of students already scheduled for the class at the given day and period.
#     This is a stub function; replace with your actual query.
#     """
#     result = cursor.execute("""
#         SELECT COUNT(*) FROM timetable
#         WHERE class_id = ? AND day = ? AND period = ?
#     """, (class_id, day, period)).fetchone()
#     return result[0] if result else 0

# def section_busy(cursor: Cursor, section_id: int, day: int, period: int) -> bool:
#     """
#     Checks if the section already has a class scheduled at the given day and period.
#     This is a stub function; replace with your actual query.
#     """
#     result = cursor.execute("""
#         SELECT 1 FROM timetable
#         JOIN section_course USING (course_code)
#         WHERE section_id = ? AND day = ? AND period = ?
#     """, (section_id, day, period)).fetchone()
#     return bool(result)

# def get_section(cursor: Cursor, **kwargs):
#     """
#     Fetch a single section record based on provided criteria.
#     This is a stub function; replace with your actual query logic.
#     """
#     # For demonstration, return a fake section record
#     return {"id": kwargs.get("id", 1), "is_lab": True, "capacity": 30, "num_students": 60}

# def get_courses(cursor: Cursor, **kwargs):
#     """
#     Fetch a course record based on provided criteria.
#     This is a stub function; replace with your actual query logic.
#     """
#     # For demonstration, return fake course data.
#     # kwargs may include elective=True/False or id=<course_code>
#     return {"id": kwargs.get("id", "C101"), "L": 3, "T": 1, "P": 2}

# # Example usage:
# if __name__ == "__main__":
#     import sqlite3
#     # Connect to a test in-memory database
#     conn = sqlite3.connect(":memory:")
#     cur = conn.cursor()

#     # Create a dummy timetable table (schema should be extended as per your needs)
#     cur.execute("""
#         CREATE TABLE timetable (
#             day INTEGER,
#             period INTEGER,
#             faculty_id INTEGER,
#             course_code TEXT,
#             class_id INTEGER
#         )
#     """)
#     # The helper functions (get_section, get_courses) are assumed to be defined elsewhere

#     # Run timetable generation for a given campus_id (e.g., 1)
#     generate_timetable(conn, cur, campus_id=1)

#     # For demonstration, show the contents of the timetable table
#     for row in cur.execute("SELECT * FROM timetable"):
#         print(row)
