from relations import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `period` (
						`id` TINYINT UNSIGNED AUTO_INCREMENT,
						`time` TIME NOT NULL,
						PRIMARY KEY(`id`)
)""")

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `timetable` (
						`day` ENUM("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday") NOT NULL,
						`period_id` TINYINT UNSIGNED NOT NULL,
						`faculty_teaches_class_id` SMALLINT UNSIGNED NOT NULL,
						PRIMARY KEY(`day`, `period_id`),
						FOREIGN KEY(`faculty_teaches_class_id`) REFERENCES `faculty_teaches_class`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT,
						FOREIGN KEY(`period_id`) REFERENCES `period`(`id`)
						ON UPDATE CASCADE ON DELETE RESTRICT
)""")

if __name__ == "__main__":
	database.close()
