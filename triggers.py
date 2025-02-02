from mysql_connector import db_connector, cursor, close

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

if __name__ == "__main__":
	close()
