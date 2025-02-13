def delete_campus(db_connector, cursor, campus):
	cursor.execute("""DELETE FROM `campuses`
				   WHERE `name`=%s""", (campus,))
	db_connector.commit()
