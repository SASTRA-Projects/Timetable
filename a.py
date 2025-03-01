import mysql_connector as s
import triggers
import views
import show_data as sd
import fetch_data as f
import insert_data as i
import add_data as a

s.connect('avnadmin', 'AVNS_QKo0x_kuhqpQdtdeiat')
views.create_views(s.db_connector, s.cursor)
triggers.create_triggers(s.db_connector, s.cursor)

# a.add_campus(s.db_connector, s.cursor, campus="SASTRA")
# a.add_campus(s.db_connector, s.cursor, campus="SRC")
# a.add_campus(s.db_connector, s.cursor, campus="Chennai Campus")
# a.add_school(s.db_connector, s.cursor, id=12, school="SRC", campus_id=sd.get_campus_id(s.cursor, campus="SRC"))
# a.add_school(s.db_connector, s.cursor, id=4, school="SoC", campus_id=sd.get_campus_id(s.cursor, campus="SASTRA"))
# a.add_school(s.db_connector, s.cursor, id=8, school="SoM", campus_id=sd.get_campus_id(s.cursor, campus="SASTRA"))

# a.add_department(s.db_connector, s.cursor, department="CSE")
# a.add_department(s.db_connector, s.cursor, department="English")
# a.add_department(s.db_connector, s.cursor, department="Physics")
# a.add_department(s.db_connector, s.cursor, department="ECE")
# a.add_department(s.db_connector, s.cursor, department="IT")
# a.add_degree(s.db_connector, s.cursor, degree="B.Tech", duration=4)
# a.add_degree(s.db_connector, s.cursor, degree="B.Sc", duration=3)
# a.add_degree(s.db_connector, s.cursor, degree="B.A", duration=3)
# a.add_degree(s.db_connector, s.cursor, degree="M.Tech", duration=2)
# a.add_stream(s.db_connector, s.cursor, stream="CSE", department="CSE")
# a.add_stream(s.db_connector, s.cursor, stream="Artificial Intelligence and Data Science", department="CSE")
# a.add_stream(s.db_connector, s.cursor, stream="Nuclear Physics", department="Physics")
# a.add_stream(s.db_connector, s.cursor, stream="ECE", department="ECE")
# a.add_programme(s.db_connector, s.cursor, degree="B.Tech", stream="Artificial Intelligence and Data Science")
# a.add_programme(s.db_connector, s.cursor, degree="B.Tech", stream="CSE")
# a.add_programme(s.db_connector, s.cursor, degree="B.Sc", stream="Nuclear Physics")
# a.add_programme(s.db_connector, s.cursor, degree="M.Tech", stream="ECE")

# a.add_school_department(s.db_connector, s.cursor, school_id=sd.get_school_id(s.cursor, school="SRC", campus_id=2), department="English")
# a.add_school_department(s.db_connector, s.cursor, school_id=sd.get_school_id(s.cursor, school="SoC", campus_id=1), department="CSE")
# a.add_school_department(s.db_connector, s.cursor, school_id=sd.get_school_id(s.cursor, school="SRC", campus_id=2), department="ECE")
# a.add_school_department(s.db_connector, s.cursor, school_id=sd.get_school_id(s.cursor, school="SoC", campus_id=1), department="IT")

# a.add_faculty(s.db_connector, s.cursor, name="Barathi S", campus_id=sd.get_campus_id(s.cursor, campus="SRC"), department="English")
# i.insert_faculty_info(s.db_connector, s.cursor, faculty_id=1, phone="9028392883", salary=80_000, password="test")
