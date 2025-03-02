from typehints import *

def create_relations(db_connector: Connection, cursor: Cursor) -> None:
	import database
	database.create_database(db_connector, cursor)

	cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_info` (
				   `faculty_id` MEDIUMINT UNSIGNED,
				   `phone` CHAR(10) NOT NULL,
				   `salary` DECIMAL(12, 2) NOT NULL,
				   `password` TINYTEXT NOT NULL,
				   PRIMARY KEY(`faculty_id`),
				   FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
				   ON UPDATE CASCADE ON DELETE CASCADE,
				   CHECK(`phone` REGEXP '^[6789][0-9]{9}$')
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_class` (
				   `id` SMALLINT UNSIGNED AUTO_INCREMENT,
				   `section_id` MEDIUMINT UNSIGNED NOT NULL,
				   `class_id` SMALLINT UNSIGNED NOT NULL, -- class is not lab
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`) 
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`section_id`),
				   UNIQUE(`class_id`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `section_students` ( -- check section class capacity
				   `section_id` MEDIUMINT UNSIGNED NOT NULL,
				   `student_id` INT UNSIGNED NOT NULL,
				   PRIMARY KEY(`section_id`, `student_id`),
				   FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`student_id`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_section_course` (
				   `id` INT UNSIGNED AUTO_INCREMENT,
				   `faculty_id` MEDIUMINT UNSIGNED NOT NULL,
				   `section_id` MEDIUMINT UNSIGNED NOT NULL,
				   `course_code` VARCHAR(10) NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `student_electives` (
				   `student_id` INT UNSIGNED NOT NULL, -- check student is in this section,
				   `course_code` VARCHAR(10) NOT NULL, -- is this course elective of this student's programme?
				   PRIMARY KEY(`student_id`, `course_code`),
				   FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	db_connector.commit()
