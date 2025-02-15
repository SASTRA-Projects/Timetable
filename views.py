def create_views(db_connector, cursor):
	import timetable
	timetable.create_timetable(db_connector, cursor)

	cursor.execute("""CREATE OR REPLACE VIEW `faculty_view` AS
                   SELECT * FROM `faculties`
                   JOIN `faculty_info`
                   ON `faculties`.`id`=`faculty_info`.`faculty_id`
    """)
	db_connector.commit()
