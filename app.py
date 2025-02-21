from flask import Flask, render_template, request, url_for, redirect, session
import secrets
import show_data
import delete_data
import mysql_connector as sql

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.before_request
def check_login():
	if not session.get("logged_in") and request.endpoint != "login" and request.endpoint != "authenticate":
		return redirect(url_for("login"))
	return True

@app.route("/login")
def login():
	if session.get("logged_in"):
		referrer = request.referrer
		if referrer:
			from urllib.parse import urlparse
			parsed_url = urlparse(referrer)
			if parsed_url.netloc == request.host:
				return redirect(referrer)
		return redirect(url_for("index"))
	return render_template("login.html", user="User", auth="/authenticate")

@app.route("/authenticate", methods=["POST"])
def authenticate():
	if request.form.get("user") and request.form.get("password"):
		try:
			while True:
				try:
					sql.connect(request.form["user"], request.form["password"])
					break
				except sql.pymysql.err.OperationalError:
					return render_template("login.html", user="User", auth="/authenticate", error_message="Invalid username or password")
				except Exception:
					return render_template("failed.html", reason="Unknown error occurred")
			import views
			views.create_views(sql.db_connector, sql.cursor)
			session["logged_in"] = True
			return redirect(url_for("index"))
		except Exception:
			return render_template("failed.html", reason="Unknown error occurred")
	return render_template("failed.html", reason="Login information not entered properly!")

@app.route("/show/faculty")
def log_faculty():
	if not session.get("faculty") or not session.get("faculty_details"):
		return render_template("login.html", user="ID", userType="number", auth="/auth_faculty", role="faculty")
	return redirect(url_for("faculty_details"))

@app.route("/auth_faculty", methods=["POST"])
def auth_faculty():
	if request.form.get("user") and request.form.get("password"):
		try:
			session["faculty_details"] = show_data.get_faculty_details(sql.cursor, request.form["user"], request.form["password"])
			session["faculty"] = True
			return redirect(url_for("faculty_details"))
		except AssertionError:
			return render_template("login.html", user="ID", userType="number", auth="/auth_faculty", role="faculty", error_message="Invalid ID")
		except Exception:
			return render_template("login.html", user="ID", userType="number", auth="/auth_faculty", role="faculty", error_message="Invalid Password")
	return render_template("failed.html", error_message="Login information not entered properly!")

@app.route("/")
@app.route("/home")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

# @app.route("/add/<string:campus>", methods=["POST"])
# def add_schools(campus):
# 	campus = request.form.get("campus")

# 	if not campus:
# 		raise Exception("Required Field: Campus name")

# 	campus = campus.strip().upper()
# 	no_of_schools = request.form.get("no_of_schools")

# 	if not (no_of_schools):
# 		raise Exception("Required Field: Number of schools")

# 	try:
# 		no_of_schools = int(no_of_schools)
# 		if not (1 <= no_of_schools <= 255):
# 			raise Exception("Range Error: Number of schools must be between 1 and 255 (both inclusive) only")
# 	except ValueError:
# 		raise Exception("Incorrect Format: Number of schools must be an integer")
	
# 	add_data.add_campus(sql.db_connector, sql.cursor, campus)
# 	return render_template("add_schools.html", campus=campus, no_of_schools=no_of_schools)

@app.route("/show/campus")
def show_campuses():
	return render_template("campus.html", function="show", campuses=show_data.show_campuses(sql.cursor))

@app.route("/show/<string:campus>")
def show_schools(campus):
	return f"{(campus)}"

# @app.route("/delete/campus")
# def delete_campus_page():
# 	return render_template("campus.html", function="delete", campuses=show_data.show_campuses(sql.cursor))

# @app.route("/delete/<string:campus>")
# def delete_campus(campus):
# 	delete_data.delete_campus(sql.db_connector, sql.cursor, campus.strip().upper())
# 	return render_template("campus.html", function="delete", campuses=show_data.show_campuses(sql.cursor))

@app.route("/show/faculty/details")
def faculty_details():
	if not session["faculty"] or not session["faculty_details"]:
		raise ValueError("Illegal access or value is missing.")
	faculty = session["faculty_details"]
	return render_template("faculty.html", faculty=faculty, campus=show_data.get_campus_name(sql.cursor, faculty["campus_id"]))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=False)
