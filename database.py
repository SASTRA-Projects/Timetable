def create_database(db_connector, cursor):
	cursor.execute("""CREATE TABLE IF NOT EXISTS `campuses` (
				   `id` TINYINT UNSIGNED AUTO_INCREMENT, -- max=255
				   `name` VARCHAR(40) NOT NULL,
				   PRIMARY KEY(`id`),
				   UNIQUE(`name`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `schools` ( -- e.g., SRC, SOC, also Library
				   `id` SMALLINT UNSIGNED AUTO_INCREMENT, -- max=65535
				   `name` VARCHAR(40) NOT NULL,
				   `campus_id` TINYINT UNSIGNED NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`campus_id`, `name`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `buildings` ( -- a school can occupy multiple buildings, many to many
				   `id` SMALLINT UNSIGNED AUTO_INCREMENT, -- max=65535
				   `school_id` SMALLINT UNSIGNED NOT NULL,
				   `no_of_rooms` SMALLINT UNSIGNED NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`school_id`) REFERENCES `schools`(`id`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `departments` ( -- e.g., CSE
				   `name` VARCHAR(40),
				   PRIMARY KEY(`name`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `degrees` ( -- e.g., B. Tech
				   `name` VARCHAR(40),
				   `duration` TINYINT UNSIGNED NOT NULL, -- in yrs <= 10
				   PRIMARY KEY(`name`),
				   CHECK(`duration` <= 10 AND `duration` >= 1)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `streams` ( -- e.g., CSE with AI
				   `name` VARCHAR(40),
				   `department` VARCHAR(40) NOT NULL,
				   PRIMARY KEY(`name`),
				   FOREIGN KEY(`department`) REFERENCES `departments`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `programmes` ( -- e.g., B. Tech (CSE with AI)
				   `id` MEDIUMINT UNSIGNED AUTO_INCREMENT,
				   `degree` VARCHAR(40) NOT NULL,
				   `stream` VARCHAR(40) NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`degree`) REFERENCES `degrees`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`stream`) REFERENCES `streams`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`degree`, `stream`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `courses` (
				   `code` VARCHAR(10),
				   `name` VARCHAR(40) NOT NULL,
				   `department` VARCHAR(40) NOT NULL,
				   `credits` TINYINT UNSIGNED NOT NULL,
				   `L` TINYINT UNSIGNED NOT NULL, -- lecture hours
				   `P` TINYINT UNSIGNED NOT NULL, -- practical hours
				   `T` TINYINT UNSIGNED NOT NULL, -- tutorial hours
				   `is_elective` BOOLEAN NOT NULL,
				   PRIMARY KEY(`code`),
				   FOREIGN KEY(`department`) REFERENCES `departments`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `campus_programmes` (
				   `campus_id` TINYINT UNSIGNED NOT NULL,
				   `programme_id` MEDIUMINT UNSIGNED NOT NULL,
				   PRIMARY KEY(`campus_id`, `programme_id`),
				   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`programme_id`) REFERENCES `programmes`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `school_departments` (
				   `school_id` SMALLINT UNSIGNED NOT NULL,
				   `department` VARCHAR(40) NOT NULL,
				   PRIMARY KEY(`school_id`, `department`),
				   FOREIGN KEY(`school_id`) REFERENCES `schools`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`department`) REFERENCES `departments`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `programme_courses` (
				   `course_code` VARCHAR(10) NOT NULL,
				   `programme_id` MEDIUMINT UNSIGNED NOT NULL,
				   PRIMARY KEY(`course_code`, `programme_id`),
				   FOREIGN KEY(`course_code`) REFERENCES `courses`(`code`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`programme_id`) REFERENCES `programmes`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `classes` (
				   `id` SMALLINT UNSIGNED AUTO_INCREMENT, -- check id <=`buildings`.`no_of_rooms`
				   `building_id` SMALLINT UNSIGNED NOT NULL,
				   `room_no` SMALLINT UNSIGNED NOT NULL,
				   `capacity` SMALLINT UNSIGNED NOT NULL, -- capacity check for students_classes
				   `is_lab` BOOLEAN NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`building_id`) REFERENCES `buildings`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`building_id`, `room_no`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `sections` (
				   `id` MEDIUMINT UNSIGNED AUTO_INCREMENT,
				   `campus_id` TINYINT UNSIGNED NOT NULL,
				   `degree` VARCHAR(40) NOT NULL,
				   `stream` VARCHAR(40),
				   `section` VARCHAR(2) NOT NULL,
				   `year` TINYINT UNSIGNED NOT NULL, -- check 0 < `year` <= `degree`.`duration`
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`degree`) REFERENCES `degrees`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`stream`) REFERENCES `streams`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `faculties` (
				   `id` MEDIUMINT UNSIGNED AUTO_INCREMENT,
				   `name` VARCHAR(40) NOT NULL,
				   `campus_id` TINYINT UNSIGNED NOT NULL,
				   `department` VARCHAR(40) NOT NULL, -- desig, salary separate, check dept in campus
				   `join_year` SMALLINT UNSIGNED NOT NULL, -- trigger to ensure join_year <= current_year
				   `phone` CHAR(10) NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`campus_id`) REFERENCES `campuses`(`id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   FOREIGN KEY(`department`) REFERENCES `departments`(`name`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   CHECK(`phone` REGEXP '^[6789][0-9]{9}$')
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `students` ( -- grades & attendance separate
				   `id` INT UNSIGNED AUTO_INCREMENT, -- e.g., max=4,294,967,296
				   `name` VARCHAR(40) NOT NULL,
				   `campus_id` TINYINT UNSIGNED NOT NULL,
				   `join_year` SMALLINT UNSIGNED NOT NULL, -- trigger to ensure join_year <= current_year
				   `programme_id` MEDIUMINT UNSIGNED NOT NULL,
				   `roll_no` SMALLINT UNSIGNED NOT NULL, -- trigger to auto_increment
				   `phone` CHAR(10) NOT NULL,
				   PRIMARY KEY(`id`),
				   FOREIGN KEY(`campus_id`, `programme_id`)
				   REFERENCES `campus_programmes`(`campus_id`, `programme_id`)
				   ON UPDATE CASCADE ON DELETE RESTRICT,
				   UNIQUE(`campus_id`, `join_year`, `programme_id`, `roll_no`),
				   CHECK(`phone` REGEXP '^[6-9][0-9]{9}$')
	)""")
	db_connector.commit()
