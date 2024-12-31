from flask import Flask, render_template, request, url_for, redirect
from retrieve_data import *

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/add/campus", methods=["GET", "POST"])
def add_campus():
	return render_template("campus.html")

# @app.route("/campus-<campus:string>")
# def display_campus(campus):
# 	show_campus(campus)

@app.route("/add/<campus>/blocks", methods=["GET", "POST"])
def add_blocks():
	campus = request.form.get("campus").strip().upper()
	no_of_blocks = int(request.form.get("no_of_blocks"))
	return render_template("block.html", campus=campus, no_of_blocks=no_of_blocks)