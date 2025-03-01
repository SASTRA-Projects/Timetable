from typehints import *

def create_views(db_connector: Connection, cursor: Cursor) -> None:
    import timetable
    timetable.create_timetable(db_connector, cursor)

    cursor.execute("""CREATE OR REPLACE VIEW `faculty_view` AS
                   SELECT * FROM `faculties`
                   JOIN `faculty_info`
                   ON `faculties`.`id`=`faculty_info`.`faculty_id`
    """)
    cursor.execute("""CREATE OR REPLACE VIEW `campus_departments` AS
                   SELECT `campuses`.`id` AS `campus_id`, `SD`.`department`
                   FROM `school_departments` `SD`
                   INNER JOIN `schools`
                   ON `schools`.`id`=`SD`.`school_id`
                   INNER JOIN `campuses`
                   ON `campuses`.`id`=`schools`.`campus_id`
    """)
    db_connector.commit()