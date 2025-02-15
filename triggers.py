def create_triggers(db_connector, cursor):
	cursor.execute("""CREATE TABLE IF NOT EXISTS `deleted_campus` (
							`id` TINYINT UNSIGNED,
							`name` VARCHAR(40),
							PRIMARY KEY(`id`)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS `deleted_blocks` (
							`id` TINYINT UNSIGNED,
							`name` VARCHAR(40),
							`campus_id` TINYINT UNSIGNED,
							PRIMARY KEY(`id`)
	)""")
	cursor.execute("""CREATE TRIGGER IF NOT EXISTS `backup_campus`
							BEFORE DELETE ON `campuses`
							FOR EACH ROW
								INSERT INTO `deleted_campus` (`id`, `name`)
								VALUES (OLD.id, OLD.name);
	""")
	db_connector.commit()
