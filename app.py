from flask import Flask, render_template, request, url_for, redirect

import timetable
import triggers
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

@app.route("/add/<campus>", methods=["POST"])
def add_blocks(campus):
	campus = request.form.get("campus")

	if not campus:
		raise Exception("Required Field: Campus name")

	campus = campus.strip().upper()
	no_of_blocks = request.form.get("no_of_blocks")

	if not (no_of_blocks):
		raise Exception("Required Field: Number of blocks")

	try:
		no_of_blocks = int(no_of_blocks)
		if not (1 <= no_of_blocks <= 255):
			raise Exception("Range Error: Number of blocks must be between 1 and 255 (both inclusive) only")
	except ValueError:
		raise Exception("Incorrect Format: Number of blocks must be an integer")
	
	add_data.add_campus(campus)
	return render_template("add_blocks.html", campus=campus, no_of_blocks=no_of_blocks)

# @app.route("/add/<campus>/<int:no_of_blocks>", methods=["POST"])
# def add_classes(campus, no_of_blocks):
# 	campus = campus.strip().upper()
# 	blocks = [f"Block {i}" for i in range(1, no_of_blocks+1)]
# 	classes = request.form.getlist("classes")

# 	if not classes:
# 		raise Exception("Required Field: Classes")

 # 	for block in blocks:
# 		for cls in classes:
# 			add_data.add_class(campus, block, cls)
# 	return render_template("add_classes.html", campus=campus, blocks=blocks)

@app.route("/show/campus")
def show_campuses():
	return render_template("campus.html", function="show", campuses=show_data.show_campuses())

@app.route("/show/<campus>")
def show_blocks(campus):
	return f"{campus}!"

@app.route("/delete/campus")
def delete_campus_page():
	return render_template("campus.html", function="delete", campuses=show_data.show_campuses())

@app.route("/delete/<campus>")
def delete_campus(campus):
	delete_data.delete_campus(campus.strip().upper())
	return render_template("campus.html", function="delete", campuses=show_data.show_campuses())

if __name__ == "__main__":
	app.run(debug=True)
