from typehints import *

def create_timetable(db_connector: Connection, cursor: Cursor) -> None:
	import relations
	relations.create_relations(db_connector, cursor)

	cursor.execute("""CREATE TABLE IF NOT EXISTS `periods` (
							`id` TINYINT UNSIGNED AUTO_INCREMENT,
							`is_break` BOOLEAN NOT NULL,
							`start_time` TIME NOT NULL,
							`end_time` TIME NOT NULL,
							PRIMARY KEY(`id`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `days` (
							`day` ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') NOT NULL,
							PRIMARY KEY(`day`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `timetables` (
							`day` ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') NOT NULL,
							`period_id` TINYINT UNSIGNED NOT NULL,
							`faculty_section_course_id` INT UNSIGNED NOT NULL,
							`class_id` SMALLINT UNSIGNED NOT NULL,
							PRIMARY KEY(`day`, `period_id`, `faculty_section_course_id`),
							FOREIGN KEY(`day`) REFERENCES `days`(`day`)
							ON UPDATE RESTRICT ON DELETE CASCADE,
							FOREIGN KEY(`faculty_section_course_id`) REFERENCES `faculty_section_course`(`id`)
							ON UPDATE CASCADE ON DELETE RESTRICT,
							FOREIGN KEY(`period_id`) REFERENCES `periods`(`id`)
							ON UPDATE CASCADE ON DELETE RESTRICT,
							FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
							ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	db_connector.commit()
