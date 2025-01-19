from flask import Flask, render_template, request, url_for, redirect

import add_data
import show_data
import delete_data

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/add/campus")
def add_campus(): 
	return render_template("add_campus.html")

@app.route("/add/<string:campus>", methods=["POST"])
def add_schools(campus):
	campus = request.form.get("campus")

	if not campus:
		raise Exception("Required Field: Campus name")

	campus = campus.strip().upper()
	no_of_schools = request.form.get("no_of_schools")

	if not (no_of_schools):
		raise Exception("Required Field: Number of schools")

	try:
		no_of_schools = int(no_of_schools)
		if not (1 <= no_of_schools <= 255):
			raise Exception("Range Error: Number of schools must be between 1 and 255 (both inclusive) only")
	except ValueError:
		raise Exception("Incorrect Format: Number of schools must be an integer")
	
	add_data.add_campus(campus)
	return render_template("add_schools.html", campus=campus, no_of_schools=no_of_schools)

@app.route("/add/<string:campus>/<int:no_of_schools>", methods=["POST"])
def add_buildings(campus, no_of_schools):
	campus = campus.strip().upper()
	schools = [f"school {i}" for i in range(1, no_of_schools+1)]
	buildings = request.form.getlist("buildings")

	if not buildings:
		raise Exception("Required Field: buildings")

	for school in schools:
		for cls in buildings:
			add_data.add_class(show_data.get_campus_id(campus), school)
	return render_template("add_buildings.html", campus=campus, schools=schools)

@app.route("/show/campus")
def show_campuses():
	return render_template("campus.html", function="show", campuses=show_data.show_campuses())

@app.route("/show/<string:campus>")
def show_schools(campus):
	return f"{campus}!"

@app.route("/delete/campus")
def delete_campus_page():
	return render_template("campus.html", function="delete", campuses=show_data.show_campuses())

@app.route("/delete/<string:campus>")
def delete_campus(campus):
	delete_data.delete_campus(campus.strip().upper())
	return render_template("campus.html", function="delete", campuses=show_data.show_campuses())

if __name__ == "__main__":
	app.run(debug=False)
