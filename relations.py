import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `tutors` (
						`faculty_id` SMALLINT UNSIGNED,
						`class_id` SMALLINT UNSIGNED,
						PRIMARY KEY(`faculty_id`, `class_id`),
						FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `faculty_teaches_class` (
						`id` SMALLINT UNSIGNED AUTO_INCREMENT,
						`faculty_id` SMALLINT UNSIGNED NOT NULL,
						`class_id` SMALLINT UNSIGNED NOT NULL,
						`subject_id` SMALLINT UNSIGNED NOT NULL,
						PRIMARY KEY(`id`),
						FOREIGN KEY(`faculty_id`) REFERENCES `faculties`(`id`),
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`subject_id`) REFERENCES `subjects`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						UNIQUE(`faculty_id`, `class_id`, `subject_id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `student_attends_class` (
						`student_id` INT UNSIGNED,
						`subject_id` SMALLINT UNSIGNED, -- check for total credit (minimum), ignoring minor electives
						`class_id` SMALLINT UNSIGNED,
						PRIMARY KEY(`student_id`, `subject_id`, `class_id`),
						FOREIGN KEY(`student_id`) REFERENCES `students`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`subject_id`) REFERENCES `subjects`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`class_id`) REFERENCES `classes`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")

if __name__ == "__main__":
	database.close()
