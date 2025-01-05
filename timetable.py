from relations import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `periods` (
						`id` TINYINT UNSIGNED AUTO_INCREMENT,
						`is_break` BOOLEAN NOT NULL,
						`start_time` TIME NOT NULL,
						`end_time` TIME NOT NULL,
						PRIMARY KEY(`id`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `days` (
						`day` ENUM("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday") NOT NULL,
						PRIMARY KEY(`day`)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `timetable` (
						`day` ENUM("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday") NOT NULL,
						`period_id` TINYINT UNSIGNED NOT NULL,
						`faculty_teaches_class_id` INT UNSIGNED NOT NULL,
						PRIMARY KEY(`day`, `period_id`),
						FOREIGN KEY(`day`) REFERENCES `days`(`day`)
						ON UPDATE RESTRICT ON DELETE CASCADE,
						FOREIGN KEY(`faculty_teaches_class_id`) REFERENCES `faculty_teaches_class`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`period_id`) REFERENCES `periods`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")

if __name__ == "__main__":
	database.close()
