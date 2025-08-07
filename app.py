# Copyright 2025 Harikrishna Srinivasan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from flask import (Flask, make_response, redirect, render_template,
                   request, session, url_for)
from typehints import NotFound, Optional, Response, Union
import fetch_data
import mysql_connector as sql
import secrets
import show_data

app = Flask(__name__, template_folder="templates")
app.jinja_env.filters.pop("attr", None)
app.jinja_env.autoescape = True
app.secret_key = secrets.token_hex(16)

DAYS: tuple[str, ...] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


@app.before_request
def check_login() -> Optional[Response]:
    if not session.get("logged_in") and request.endpoint != "login" \
       and request.endpoint != "authenticate":
        return redirect(url_for("login"))
    return None


def nocache(view):
    def no_cache_response(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, " \
                                            "must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    no_cache_response.__name__ = view.__name__
    return no_cache_response


@app.route("/login", methods=["GET", "POST"])
@nocache
def login() -> Union[Response, str]:
    if request.method == "GET":
        if session.get("logged_in"):
            return redirect(url_for("index"))
        else:
            return render_template("login.html", user="User",
                                   auth="/login", role="User")

    elif request.form.get("user") and request.form.get("password"):
        try:
            sql.connect(user=request.form["user"],
                        password=request.form["password"])
            if sql.db_connector and sql.cursor:
                session["logged_in"] = True
            return redirect(url_for("index"))
        except sql.pymysql.err.OperationalError:
            return render_template("login.html",
                                   user="User",
                                   auth="/authenticate",
                                   error_message="Invalid username"
                                   "or password",
                                   role="User")
        except Exception:
            return render_template("failed.html",
                                   reason="Unknown error occurred")
    return render_template("failed.html",
                           reason="Login information not entered properly!")


@app.route("/faculty")
@nocache
def log_faculty() -> Union[Response, str]:
    if not session.get("faculty") or not session.get("faculty_details"):
        return render_template("login.html", user="ID", userType="number",
                               auth="/auth_faculty", role="faculty")
    return redirect(url_for("faculty_details"))


@app.route("/auth_faculty", methods=["POST"])
def auth_faculty() -> Union[Response, str]:
    if (user := request.form.get("user")) \
       and (password := request.form.get("password")):
        try:
            if sql.cursor:
                session["faculty_details"] = fetch_data.get_faculty_details(
                                                sql.cursor,
                                                id=int(user),
                                                password=password)
                session["faculty"] = True
                return redirect(url_for("show_faculty_details"))
            return render_template("failed.html", reason="Unauthorized Login!")
        except AssertionError:
            return render_template("login.html", user="ID", userType="number",
                                   auth="/auth_faculty", role="faculty",
                                   error_message="Invalid ID or Password")
        except Exception:
            return render_template("login.html", user="ID", userType="number",
                                   auth="/auth_faculty", role="faculty",
                                   error_message="Invalid ID")
    return render_template("failed.html",
                           reason="Login information not entered properly!")


@app.route("/home")
@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/campus")
def show_campuses() -> str:
    if sql.cursor:
        return render_template("campus.html",
                               campuses=show_data.get_campuses(sql.cursor))
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/campus/<string:campus>")
def show_schools(campus: str) -> str:
    if sql.cursor:
        campus_id = show_data.get_campus_id(sql.cursor, campus=campus)
        if campus_id is None:
            return render_template("failed.html",
                                   reason="No such Campus found!!")
        return render_template("school.html",
                               schools=show_data.get_schools(
                                                sql.cursor,
                                                campus_id=campus_id),
                               campus=campus)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/school/<string:campus>/<string:school>")
def show_buildings(campus: str, school: str) -> str:
    if sql.cursor:
        campus_id = show_data.get_campus_id(sql.cursor, campus=campus)
        if campus_id is None:
            return render_template("failed.html",
                                   reason="No such Campus found!!")
        school_id = show_data.get_school_id(sql.cursor, campus_id=campus_id,
                                            school=school)
        if school_id is None:
            return render_template("failed.html",
                                   reason=f"No such School found in {campus}!")
        return render_template("building.html",
                               buildings=show_data.get_buildings(
                                   sql.cursor,
                                   school_id=school_id),
                               school=school)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/degree")
def show_degrees() -> str:
    if sql.cursor:
        return render_template("degree.html",
                               degrees=show_data.get_degrees(sql.cursor))
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/programme")
def show_programmes() -> str:
    if sql.cursor:
        return render_template("programme.html",
                               programmes=show_data.get_programmes(sql.cursor))
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/degree/<string:degree>")
def show_degree_programmes(degree: str) -> str:
    if sql.cursor:
        programmes = show_data.get_programmes(sql.cursor, degree=degree)
        return render_template("stream.html",
                               degree=degree, streams=programmes)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>")
def show_years(degree: str, stream: str) -> str:
    if sql.cursor:
        duration = show_data.get_degree_duration(sql.cursor, degree=degree)
        if not isinstance(duration, int):
            raise TypeError("Duration expected as int not as "
                            f"{type(duration).__name__}")
        return render_template("year.html", degree=degree, stream=stream,
                               years=range(1, duration+1))
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>")
def show_programme_campuses(degree: str, stream: str, year: int) -> str:
    if sql.cursor:
        programme_id = show_data.get_programme_id(sql.cursor,
                                                  degree=degree, stream=stream)
        campuses = show_data.get_campuses(sql.cursor,
                                          programme_id=programme_id)
        return render_template("programme_campus.html", campuses=campuses,
                               degree=degree, stream=stream, year=year)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>", methods=["POST"])
def show_sections(degree: str, stream: str, year: int) -> str:
    if sql.cursor:
        campus_id = int(request.form["campus_id"])
        sections = fetch_data.get_sections(sql.cursor, campus_id=campus_id,
                                           degree=degree, stream=stream,
                                           year=year)
        return render_template("section.html", degree=degree, stream=stream,
                               year=year, sections=sections)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>/<string:section>",
           methods=["POST"])
def show_courses(degree: str, stream: str, year: int, section: str) -> str:
    if sql.cursor:
        section_id = int(request.form["section_id"])
        faculty_courses = fetch_data.get_faculty_section_courses(
                            sql.cursor,
                            section_id=section_id)
        courses = {}
        for fc in faculty_courses:
            course_code = fc["course_code"]
            if course_code in courses:
                continue
            courses[course_code] = fetch_data.get_course(sql.cursor,
                                                         code=course_code)
            courses[course_code].update(
                {"is_elective": "Department Elective" if
                                fetch_data.is_elective(sql.cursor,
                                                       course_code=course_code,
                                                       section_id=section_id)
                                else "Department Core"})
        return render_template("course.html", courses=courses,
                               degree=degree, stream=stream,
                               year=year, section=section,
                               section_id=section_id)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/faculty/details")
def show_faculty_details() -> str:
    if sql.cursor:
        if not session.get("faculty") or not session.get("faculty_details"):
            return render_template("failed.html",
                                   reason="Illegal access or value is missing")
        faculty = session["faculty_details"]
        campus = show_data.get_campus_name(sql.cursor, id=faculty["campus_id"])
        return render_template("faculty.html", faculty=faculty, campus=campus)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/faculty/timetable")
def show_faculty_timetable() -> str:
    if sql.cursor:
        if not session.get("faculty") or not session.get("faculty_details"):
            return render_template("failed.html",
                                   reason="Illegal access or value is missing")
        id = session["faculty_details"]["id"]
        if faculty := fetch_data.get_faculty_name(sql.cursor, id=id):
            pass

        periods = fetch_data.get_periods(sql.cursor)
        for period in periods:
            period["time_range"] = f"{period['start_time']}-{period['end_time']}"

        grid = {day: {period["id"]: "" for period in periods} for day in DAYS}
        timetables = fetch_data.get_timetables(sql.cursor, faculty_id=id)
        for row in timetables:
            day = row["day"]
            period_id = row["period_id"]
            content = f"{row['course_code']}-{row['faculty_id']}({row['room_no']})"
            if row["is_lab"]:
                content += "(Lab)"
            if content:
                if grid[day][period_id]:
                    grid[day][period_id] += "/"
                grid[day][period_id] += content

        course_data = {}
        for fc in timetables:
            course_code = fc["course_code"]
            course = fetch_data.get_course(sql.cursor, code=course_code)
            if course_code not in course_data:
                course_data[course_code] = {
                    "name": course["name"],
                    "faculties": set(),
                    "credits": course["credits"],
                    "L": course["L"],
                    "P": course["P"],
                    "T": course["T"],
                }
            course_data[course_code]["faculties"].add(f"{faculty}({fc['faculty_id']})")

        for course in course_data.values():
            course["faculties"] = ", ".join(course["faculties"])

        title = "Timetable"
        return render_template("timetable.html", title=title, days=DAYS, periods=periods, grid=grid, course_data=course_data)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/timetable", methods=["POST"])
def show_timetables() -> str:
    if sql.cursor:
        section_id = int(request.form["section_id"])
        periods = fetch_data.get_periods(sql.cursor)
        section = fetch_data.get_section(sql.cursor, section_id=section_id)
        campus = show_data.get_campus_name(sql.cursor, id=section["campus_id"])
        title = f"{campus}-{section['degree']} {section['stream'] or ''} {section['section']} (Year {section['year']})"
        for period in periods:
            period["time_range"] = f"{period['start_time']}-{period['end_time']}"
        grid = {day: {period["id"]: "" for period in periods} for day in DAYS}
        timetables = fetch_data.get_timetables(sql.cursor, section_id=section_id)
        for row in timetables:
            day = row["day"]
            period_id = row["period_id"]
            content = f"{row['course_code']}-{row['faculty_id']}({row['room_no']})"
            if row["is_lab"]:
                content += "(Lab)"
            if content:
                if grid[day][period_id]:
                    grid[day][period_id] += "/"
                grid[day][period_id] += content

        course_data = {}
        for fc in timetables:
            faculty = fetch_data.get_faculty_name(sql.cursor,
                                                  id=fc["faculty_id"])
            course_code = fc["course_code"]
            course = fetch_data.get_course(sql.cursor, code=course_code)
            if course_code not in course_data:
                course_data[course_code] = {
                    "name": course["name"],
                    "faculties": set(),
                    "credits": course["credits"],
                    "L": course["L"],
                    "P": course["P"],
                    "T": course["T"],
                }
            course_data[course_code]["faculties"].add(f"{faculty}({fc['faculty_id']})")

        for course in course_data.values():
            course["faculties"] = ", ".join(course["faculties"])
        return render_template("timetable.html", days=DAYS, periods=periods, grid=grid, course_data=course_data, title=title)
    return render_template("failed.html", reason="Unknown error occurred")


@app.route("/logout")
def logout() -> Response:
    session.clear()
    sql.close()
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error: NotFound) -> tuple[str, int]:
    return (render_template("404.html"), 404)


if __name__ == "__main__":
    app.config.update(
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True
    )
    app.run(host="0.0.0.0", port=5000, debug=False)
