import database

database.cursor.execute("""CREATE TABLE IF NOT EXISTS `deleted_campus` (
						`id` TINYINT UNSIGNED,
						`name` VARCHAR(40)
)""")
database.cursor.execute("""CREATE TABLE IF NOT EXISTS `deleted_blocks` (
						`id` TINYINT UNSIGNED,
						`name` VARCHAR(40),
						`campus_id` TINYINT UNSIGNED
)""")

database.cursor.execute("""CREATE TRIGGER IF NOT EXISTS `backup_campus`
						BEFORE DELETE ON `campuses`
						FOR EACH ROW
							INSERT INTO `deleted_campus` (`id`, `name`)
							VALUES (OLD.id, OLD.name);
""")