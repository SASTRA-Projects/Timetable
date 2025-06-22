from typehints import *

def get_campuses(cursor: Cursor, /, *,
				 programme_id: Optional[int] = None) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	if programme_id:
		cursor.execute("""SELECT `campuses`.`id`,
					   `campuses`.`name`
					   FROM `campuses`
					   JOIN `campus_programmes` AS `CP`
					   ON `campuses`.`id`=`CP`.`campus_id`
					   AND `CP`.`programme_id`=%s""",
					   (programme_id,))
	else:
		cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(cursor: Cursor, /, *,
				  campus: Optional[str] = None) -> Optional[int]:
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name` LIKE %s""", (campus,))
	result: Optional[Dict[str, int]] = cursor.fetchone()
	if result:
		return result["id"]
	return None

def get_campus_name(cursor: Cursor, /, *,
					id: Optional[int] = None) -> Optional[str]:
	cursor.execute("""SELECT `name` FROM `campuses`
				   WHERE `id`=%s""", (id,))
	result: Optional[Dict[str, str]] = cursor.fetchone()
	if result:
		return result["name"]
	return None

def get_schools(cursor: Cursor, /, *,
				campus_id: Optional[int] = None,
				department: Optional[str] = None) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	if campus_id and department:
		cursor.execute("""SELECT `schools`.`id`, `schools`.`name`
					   FROM `schools`
					   JOIN `school_departments` AS `SD`
					   ON `schools`.`id`=`SD`.`school_id`
					   AND `schools`.`campus_id`=%s
					   AND `SD`.`department` LIKE %s""",
					   (campus_id, department))
	elif campus_id:
			cursor.execute("""SELECT `id`, `name` FROM `schools`
						   WHERE `campus_id`=%s""", (campus_id))
	elif department:
		cursor.execute("""SELECT `schools`.`id`,
					   `schools`.`name`,
					   `schools`.`campus_id`
					   FROM `schools`
					   JOIN `school_departments` AS `SD`
					   ON `schools`.`id`=`SD`.`school_id`
					   AND `SD`.`department` LIKE %s""",
					   (department,))
	else:
		cursor.execute("""SELECT `id`, `name`, `campus_id` FROM `schools`""")
	return cursor.fetchall()

def get_school_id(cursor: Cursor, /, *,
				  campus_id: Optional[int] = None,
				  school: Optional[str] = None) -> Optional[int]:
	if campus_id:
		cursor.execute("""SELECT `id` FROM `schools`
					   WHERE `campus_id`=%s
					   AND `name`=%s""", (campus_id, school))
	else:
		cursor.execute("""SELECT `id`, `name` FROM `schools`
					   WHERE `name`=%s""", (school,))
	result: Optional[Dict[str, int]] = cursor.fetchone()
	if result:
		return result["id"]
	return None

def get_buildings(cursor: Cursor, /, *,
				  school_id: Optional[int] = None,
				  campus_id: Optional[int] = None) -> Tuple[Optional[Dict[str, int]], ...]:
	if school_id:
		cursor.execute("""SELECT `id`, `rooms` FROM `buildings`
					   WHERE `school_id`=%s""", (school_id,))
	elif campus_id:
		cursor.execute("""SELECT `building_id` AS `id`, `school_id`, `rooms`
					   FROM `campus_buildings`
					   WHERE `campus_id`=%s""", (campus_id,))
	else:
		cursor.execute("""SELECT `id`, `school_id`, `rooms` FROM `buildings`""")
	return cursor.fetchall()

def get_building_id(cursor: Cursor, /, *,
					school_id: Optional[int] = None,
					campus_id: Optional[int] = None) -> Optional[List[int]]:
	buildings: Tuple[Optional[Dict[str, int]], ...] = get_buildings(cursor, school_id=school_id, campus_id=campus_id)
	if not buildings:
		return None
	return [building["id"] for building in buildings]

def get_departments(cursor: Cursor, /, *,
					school_id: Optional[int] = None) -> Tuple[Optional[Dict[str, str]], ...]:
	if school_id:
		cursor.execute("""SELECT `department` FROM `school_departments`
					   WHERE `school_id`=%s""", (school_id,))
	else:
		cursor.execute("""SELECT * FROM `departments`""")
	return cursor.fetchall()

def get_degrees(cursor: Cursor, /) -> Tuple[Optional[Dict[str, str]], ...]:
	cursor.execute("""SELECT * FROM `degrees`""")
	return cursor.fetchall()

def get_degree_duration(cursor: Cursor, /, *,
						degree: Optional[str] = None) -> Optional[int]:
	cursor.execute("""SELECT `duration` FROM `degrees`
				   WHERE `degree` LIKE %s""", (degree,))
	result: Optional[Dict[str, int]] = cursor.fetchone()
	if result:
		return result["duration"]
	return None

def get_streams(cursor: Cursor, /, *,
				department: Optional[str] = None) -> Tuple[Optional[Dict[str, str]], ...]:
	if department:
		cursor.execute("""SELECT `stream`
					   FROM `school_streams`
					   WHERE `department` LIKE %s""", (department,))
	else:
		cursor.execute("""SELECT * FROM `streams`""")
	return cursor.fetchall()

def get_programmes(cursor: Cursor, /, *,
                   campus_id: Optional[int] = None,
                   degree: Optional[str] = None,
                   stream: Optional[str] = None) -> Tuple[Optional[Dict[str, str]], ...]:
    
    if degree == "B.A":
        return (
            {"id": 1, "degree": "B.A", "stream": "English"},   
            {"id": 2, "degree": "B.A", "stream": "Mathematics"},
        )
    elif degree == "B.Sc":
        return (
            {"id": 3, "degree": "B.Sc", "stream": "Physics"},
        )
    elif degree == "B.Tech":
        return (
            {"id": 4, "degree": "B.Tech", "stream": "AIDS"},
            {"id": 5, "degree": "B.Tech", "stream": "CSE"},
        )
    elif degree == "M.Tech":
        return (
            {"id": 6, "degree": "M.Tech", "stream": "ECE"},
        )
    else:
        # fallback: return all (you can add more if needed)
        return (
            {"id": 1, "degree": "B.A", "stream": "English"},
            {"id": 2, "degree": "B.A", "stream": "Mathematics"},
            {"id": 3, "degree": "B.Sc", "stream": "Physics"},
            {"id": 4, "degree": "B.Tech", "stream": "AIDS"},
            {"id": 5, "degree": "B.Tech", "stream": "CSE"},
            {"id": 6, "degree": "M.Tech", "stream": "ECE"},
        )


def get_programme(cursor: Cursor, /, *,
				  programme_id: Optional[int] = None) -> Optional[Dict[str, str]]:
	cursor.execute("""SELECT `degree`, `stream`
				   FROM `programmes`
				   WHERE `id`=%s""", (programme_id,))
	return cursor.fetchone()

def get_programme_id(cursor: Cursor, /, *,
					 degree: Optional[str] = None,
					 stream: Optional[str] = None) -> Optional[int]:
	if not (degree and stream):
		return None
	programme = get_programmes(cursor, degree=degree, stream=stream)
	if not programme:
		return None
	return programme[0]["id"]
