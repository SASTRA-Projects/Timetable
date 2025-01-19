import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `section_classes` (
						`id` SMALLINT UNSIGNED AUTO_INCREMENT,
						`section_id` MEDIUMINT UNSIGNED NOT NULL,
						`class_id` SMALLINT UNSIGNED NOT NULL, -- class is not lab
						PRIMARY KEY(`id`),
						FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`) 
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`section_id`, `class_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `section_lab_classes` (
						`id` SMALLINT UNSIGNED AUTO_INCREMENT,
						`section_id` MEDIUMINT UNSIGNED NOT NULL,
						`class_id` SMALLINT UNSIGNED NOT NULL, -- class is lab
						PRIMARY KEY(`id`),
						FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`) 
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`section_id`, `class_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `student_sections` ( -- check section class capacity
						`student_id` INT UNSIGNED NOT NULL,
						`section_class_id` SMALLINT UNSIGNED NOT NULL,
						PRIMARY KEY(`student_id`, `section_class_id`),
						FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`section_class_id`) REFERENCES `section_classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`student_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `section_courses` (
						`id` INT UNSIGNED AUTO_INCREMENT,
						`section_id` MEDIUMINT UNSIGNED NOT NULL,
						`course_code` VARCHAR(10) NOT NULL,
						PRIMARY KEY(`id`),
						FOREIGN KEY(`section_id`) REFERENCES `sections`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`) 
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`section_id`, `course_code`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_teaches_section` (
						`id` INT UNSIGNED AUTO_INCREMENT,
						`faculty_id` MEDIUMINT UNSIGNED NOT NULL,
						`section_course_id` INT UNSIGNED NOT NULL,
						PRIMARY KEY(`id`),
						FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`section_course_id`) REFERENCES `section_courses`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `student_attends_class` (
						`student_id` INT UNSIGNED NOT NULL, -- check student in this section has,
						`course_code` VARCHAR(10) NOT NULL, -- this course?
						PRIMARY KEY(`student_id`, `course_code`),
						FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")

if __name__ == "__main__":
	database.close()
