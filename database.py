from mysql_connect import cursor, db_connector, close

cursor.execute("""CREATE DATABASE IF NOT EXISTS `SASTRA`""")
cursor.execute("""USE `SASTRA`""")

cursor.execute("""CREATE TABLE IF NOT EXISTS `campuses` (
			   `id` TINYINT UNSIGNED AUTO_INCREMENT,
			   `name` VARCHAR(40) NOT NULL,
			   PRIMARY KEY(`id`)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `blocks` (
			   `id` TINYINT UNSIGNED AUTO_INCREMENT,
			   `name` VARCHAR(40) NOT NULL,
			   `campus_id` TINYINT UNSIGNED NOT NULL,
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `classes` (
			   `id` SMALLINT UNSIGNED AUTO_INCREMENT,
			   `block_id` TINYINT UNSIGNED NOT NULL,
			   `room_no` SMALLINT UNSIGNED NOT NULL,
			   `capacity` SMALLINT UNSIGNED NOT NULL,
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`block_id`) REFERENCES `blocks`(`id`),
			   UNIQUE(`block_id`, `room_no`)

)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `departments` (
			   `id` SMALLINT UNSIGNED AUTO_INCREMENT,
			   `name` VARCHAR(40) NOT NULL,
			   PRIMARY KEY(`id`)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `courses` (
			   `id` SMALLINT UNSIGNED AUTO_INCREMENT,
			   `name` VARCHAR(40) NOT NULL,
			   `department_id` SMALLINT UNSIGNED NOT NULL,
			   `duration` TINYINT UNSIGNED NOT NULL, -- in years
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`department_id`) REFERENCES `departments`(`id`)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `subjects` (
			   `id` SMALLINT UNSIGNED,
			   `name` VARCHAR(40) NOT NULL,
			   `department_id` SMALLINT UNSIGNED NOT NULL,
			   `credits` TINYINT UNSIGNED NOT NULL,
			   `type` ENUM("Theory", "Lab", "Semi-Theory Semi-Lab") NOT NULL,
			   `is_elective` BOOLEAN NOT NULL,
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`department_id`) REFERENCES `departments`(`id`)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS `students` ( -- grades & attendance separate
			   `id` INT UNSIGNED AUTO_INCREMENT,
			   `campus_id` TINYINT UNSIGNED NOT NULL,
			   `join_year` TINYINT UNSIGNED NOT NULL, -- trigger to ensure join_year <= current_year
			   `course_id` SMALLINT UNSIGNED NOT NULL,
			   `roll_no` SMALLINT UNSIGNED NOT NULL, -- trigger to auto_increment
			   `name` VARCHAR(40) NOT NULL,
			   `phone` CHAR(10) NOT NULL,
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`),
			   FOREIGN KEY(`course_id`) REFERENCES `courses`(`id`),
			   UNIQUE(`campus_id`, `join_year`, `course_id`, `roll_no`)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `faculties` (
			   `id` SMALLINT UNSIGNED AUTO_INCREMENT,
			   `name` VARCHAR(40) NOT NULL,
			   `phone` CHAR(10) NOT NULL,
			   `campus_id` TINYINT UNSIGNED NOT NULL,
			   `department_id` SMALLINT UNSIGNED NOT NULL, -- desig, salary separate
			   PRIMARY KEY(`id`),
			   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`),
			   FOREIGN KEY(`department_id`) REFERENCES `departments`(`id`)
)""")

db_connector.commit()

if __name__ == "__main__":
	close()
