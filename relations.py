import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `student_sections` ( -- can be attr. in `students`
						`student_id` INT UNSIGNED,
						`section_id` MEDIUMINT UNSIGNED NOT NULL,
						PRIMARY KEY(`student_id`, `section_id`),
						FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`student_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `section_courses` (
						`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
						`section_id` MEDIUMINT UNSIGNED NOT NULL,
						`course_code` VARCHAR(10) NOT NULL,
						PRIMARY KEY(`id`),
						FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`) 
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`section_id`, `course_code`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_teaches_class` (
						`id` INT UNSIGNED AUTO_INCREMENT,
						`faculty_id` MEDIUMINT UNSIGNED NOT NULL,
						`class_id` SMALLINT UNSIGNED NOT NULL,
						`section_course_id` INT UNSIGNED NOT NULL,
						PRIMARY KEY(`id`),
						FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`section_course_id`) REFERENCES `section_courses`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`faculty_id`, `class_id`, `section_course_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `student_attends_class` (
						`student_id` INT UNSIGNED NOT NULL,
						`course_code` VARCHAR(10) NOT NULL,
						`class_id` SMALLINT UNSIGNED NOT NULL,
						PRIMARY KEY(`student_id`, `course_code`, `class_id`),
						FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")

if __name__ == "__main__":
	database.close()
