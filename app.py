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
from flask_compress import Compress
from typehints import NotFound, Optional, Response, Union
import fetch_data
import insert_data
import mysql_connector as sql
import secrets
import show_data

app = Flask(__name__, template_folder="templates")
app.jinja_env.filters.pop("attr", None)
app.jinja_env.autoescape = True
app.secret_key = secrets.token_hex(16)
Compress(app)
app.config['COMPRESS_MIMETYPES'] = ['application/json', 'text/css', 'text/html', 'text/plain']
app.config['COMPRESS_LEVEL'] = 9

DAYS: tuple[str, ...] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
timetables: list[dict[str, Union[bool, int, str]]] = []


@app.before_request
def check_login(login: str = "login") -> Optional[Response]:
    if not session.get("logged_in") and request.endpoint != login:
        return redirect(url_for(login))
    return None


def nocache(view):
    def no_cache_response(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    no_cache_response.__name__ = view.__name__
    return no_cache_response


@app.route("/login", methods=["GET", "POST"])
@nocache
def login(
    index: str = "index",
) -> Union[Response, str]:
    if request.method == "GET":
        if session.get("logged_in"):
            return redirect(url_for(index))
        else:
            return render_template("./login.html", user="User",
                                   auth="/login", role="User")

    elif request.form.get("user") and request.form.get("password"):
        try:
            sql.connect(user=request.form["user"],
                        password=request.form["password"])
            if sql.db_connector and sql.cursor:
                session["logged_in"] = True
            return redirect(url_for(index))
        except sql.pymysql.err.OperationalError:
            return render_template(
                "./login.html",
                user="User",
                auth="/login",
                error_message="Invalid username or password",
                role="User")
        except Exception:
            return render_template("./failed.html",
                                   reason="Unknown error occurred")
    return render_template("./failed.html",
                           reason="Login information not entered properly!")


@app.route("/faculty")
@nocache
def log_faculty() -> Union[Response, str]:
    if not session.get("faculty") or not session.get("faculty_details"):
        return render_template("./login.html", user="ID",
                               auth="/auth_faculty", role="faculty")
    return redirect(url_for("faculty_details"))


@app.route("/auth_faculty", methods=["POST"])
def auth_faculty() -> Union[Response, str]:
    if (user := request.form.get("user")) \
       and (password := request.form.get("password")):
        try:
            if sql.cursor:
                session["faculty_details"] = fetch_data.get_faculty_details(
                                                sql.cursor, id=user,
                                                password=password)
                session["faculty"] = True
                return redirect(url_for("show_faculty_details"))
            return render_template("./failed.html", reason="Unauthorized Login!")
        except AssertionError:
            return render_template("./login.html", user="ID", userType="number",
                                   auth="/auth_faculty", role="faculty",
                                   error_message="Invalid ID or Password")
        except Exception:
            return render_template("./login.html", user="ID", userType="number",
                                   auth="/auth_faculty", role="faculty",
                                   error_message="Invalid ID")
    return render_template("./failed.html",
                           reason="Login information not entered properly!")


@app.route("/home")
@app.route("/")
def index() -> str:
    return render_template("./index.html")


@app.route("/about")
def about() -> str:
    return render_template("./about.html")


@app.route("/campus")
def show_campuses() -> str:
    if sql.cursor:
        campuses = sorted(show_data.get_campuses(sql.cursor),
                          key=lambda campus: campus["id"])
        return render_template("./campus.html",
                               campuses=campuses)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/campus/<string:campus>")
def show_schools(campus: str) -> str:
    if sql.cursor:
        campus_id = show_data.get_campus_id(sql.cursor, campus=campus)
        if campus_id is None:
            return render_template("./failed.html",
                                   reason="No such Campus found!!")
        return render_template("./school.html",
                               schools=show_data.get_schools(
                                                sql.cursor,
                                                campus_id=campus_id),
                               campus=campus)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/school/<string:campus>/<string:school>")
def show_buildings(campus: str, school: str) -> str:
    if sql.cursor:
        campus_id = show_data.get_campus_id(sql.cursor, campus=campus)
        if campus_id is None:
            return render_template("./failed.html",
                                   reason="No such Campus found!!")
        school_id = show_data.get_school_id(sql.cursor, campus_id=campus_id,
                                            school=school)
        if school_id is None:
            return render_template("./failed.html",
                                   reason=f"No such School found in {campus}!")
        return render_template("./building.html",
                               buildings=show_data.get_buildings(
                                   sql.cursor,
                                   school_id=school_id),
                               school=school)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/degree")
def show_degrees() -> str:
    if sql.cursor:
        return render_template("./degree.html",
                               degrees=show_data.get_degrees(sql.cursor))
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/programme")
def show_programmes() -> str:
    if sql.cursor:
        return render_template("./programme.html",
                               programmes=show_data.get_programmes(sql.cursor))
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/degree/<string:degree>")
def show_degree_programmes(degree: str) -> str:
    if sql.cursor:
        programmes = show_data.get_programmes(sql.cursor, degree=degree)
        if None in {p["stream"] for p in programmes}:
            return redirect(f"/{degree}/None")
        return render_template("./stream.html",
                               degree=degree, streams=programmes)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>")
def show_years(degree: str, stream: str) -> str:
    if sql.cursor:
        duration = show_data.get_degree_duration(sql.cursor, degree=degree)
        if not isinstance(duration, int):
            raise TypeError("Duration expected as int not as "
                            f"{type(duration).__name__}")
        return render_template("./year.html", degree=degree, stream=stream,
                               years=range(1, duration+1))
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>")
def show_programme_campuses(degree: str, stream: str, year: int) -> str:
    if sql.cursor:
        programme_id = show_data.get_programme_id(sql.cursor,
                                                  degree=degree, stream=stream)
        campuses = show_data.get_campuses(sql.cursor,
                                          programme_id=programme_id)
        return render_template("./programme_campus.html", campuses=campuses,
                               degree=degree, stream=stream, year=year)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>", methods=["POST"])
def show_sections(degree: str, stream: str, year: int) -> str:
    if sql.cursor:
        campus_id = int(request.form["campus_id"])
        sections = fetch_data.get_sections(sql.cursor, campus_id=campus_id,
                                           degree=degree, stream=stream,
                                           year=year)
        return render_template("./section.html", degree=degree, stream=stream,
                               year=year, sections=sections)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/<string:degree>/<string:stream>/<int:year>/<string:section>", methods=["POST"])
def show_courses(degree: str, stream: str, year: int, section: str) -> str:
    if sql.cursor:
        section_id = int(request.form["section_id"])
        faculty_courses = fetch_data.get_faculty_section_courses(
            sql.cursor,
            section_id=section_id
        )

        courses: dict[str, dict] = {}
        for fc in faculty_courses:
            assert isinstance(fc["hrs"], int) and isinstance(fc["full_batch"], int)
            assert isinstance(fc["course_code"], str)

            course_code = fc["course_code"]
            hrs_contribution = 0
            if fc["is_lab"] and not fc["full_batch"]:
                hrs_contribution = fc["hrs"] / 4
            elif fc["is_lab"]:
                hrs_contribution = fc["hrs"] / 2
            elif course_code not in courses:
                hrs_contribution = fc["hrs"]

            if course_code in courses:
                if course_code in ("CHY101", "CIV103"):
                    courses[course_code]["hrs"] = 5
                elif not hrs_contribution:
                    courses[course_code]["hrs"] = max(courses[course_code]["hrs"], fc["hrs"])
                else:
                    courses[course_code]["hrs"] += hrs_contribution
            else:
                courses[course_code] = fc.copy()
                courses[course_code]["hrs"] = hrs_contribution
                label = "Department Elective" if fc["is_elective"] else "Department Core"
                courses[course_code]["is_elective"] = label
            if course_code == "CIV102":
                print(courses[course_code], fc, hrs_contribution)

        return render_template("./course.html", 
                               courses=courses,
                               degree=degree, 
                               stream=stream,
                               year=year, 
                               section=section,
                               section_id=section_id)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/faculty/details")
def show_faculty_details() -> str:
    if sql.cursor:
        if not session.get("faculty") or not session.get("faculty_details"):
            return render_template("./failed.html",
                                   reason="Illegal access or value is missing")
        faculty = session["faculty_details"]
        campus = show_data.get_campus_name(sql.cursor, id=faculty["campus_id"])
        return render_template("./faculty.html", faculty=faculty, campus=campus)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/faculty/timetable")
def show_faculty_timetable() -> str:
    if sql.cursor:
        global timetables
        if not session.get("faculty") or not session.get("faculty_details"):
            return render_template("./failed.html",
                                   reason="Illegal access or value is missing")
        id = session["faculty_details"]["id"]
        faculty = fetch_data.get_faculty_name(sql.cursor, id=id)
        if not faculty:
            return render_template("./failed.html", reason="Faculty not found")

        periods = fetch_data.get_periods(sql.cursor)
        for period in periods:
            period["time_range"] = f"{period['start_time']}-{period['end_time']}"

        grid = {day: {period["id"]: "" for period in periods} for day in DAYS}

        if not timetables:
            timetables = fetch_data.get_timetables(sql.cursor)

        _timetables = [t for t in timetables if t["faculty_id"] == id]

        for row in _timetables:
            day = row["day"]
            period_id = row["period_id"]
            section = fetch_data.get_section(sql.cursor, section_id=row["section_id"])
            sec_name = f"{section['degree']} {section['stream'] or ''} {section['year']}{section['section']}"
            content = f"{row['course_code']}-{sec_name}({row['room_no']})"
            if row["is_lab"]:
                content += "(Lab)"
            if content:
                if grid[day][period_id]:
                    grid[day][period_id] += " / "
                grid[day][period_id] += content

        course_data = {}
        for fc in _timetables:
            course_code = fc["course_code"]
            if course_code not in course_data:
                course = fetch_data.get_course(sql.cursor, code=course_code)
                course_data[course_code] = {
                    "name": course["name"],
                    "faculties": set(),
                    "hrs": 0
                }

            course_data[course_code]["hrs"] += 1
            course_data[course_code]["faculties"].add(faculty)

        for course in course_data.values():
            course["faculties"] = ", ".join(course["faculties"])

        title = f"Timetable - {faculty} ({id})"
        return render_template("./timetable.html", title=title, days=DAYS,
                               periods=periods, grid=grid, course_data=course_data)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/timetable", methods=["POST"])
def show_timetables() -> str:
    if sql.cursor:
        global timetables
        section_id = int(request.form["section_id"])
        periods = fetch_data.get_periods(sql.cursor)
        section = fetch_data.get_section(sql.cursor, section_id=section_id)
        campus = show_data.get_campus_name(sql.cursor, id=section["campus_id"])
        title = f"{campus}-{section['degree']} {section['stream'] or ''} {section['section']} (Year {section['year']})"
        for period in periods:
            period["time_range"] = f"{period['start_time']}-{period['end_time']}"

        grid = {day: {period["id"]: "" for period in periods} for day in DAYS}
        if not timetables:
            timetables = fetch_data.get_timetables(sql.cursor)

        _timetables = [t for t in timetables if t["section_id"] == section_id]
        course_data: dict[str, dict[str, Union[int, str]]] = {}
        for row in _timetables:
            day = row["day"]
            period_id = row["period_id"]
            content = f"{row['course_code']}-{row['faculty_id']}({row['room_no']})"
            if row["is_lab"]:
                content += "(Lab)"

            if content:
                if grid[day][period_id]:
                    if content not in grid[day][period_id]:
                        grid[day][period_id] += " / " + content
                else:
                    grid[day][period_id] = content

            course_code = row["course_code"]
            faculty_name = fetch_data.get_faculty_name(sql.cursor, id=row["faculty_id"])
            if course_code not in course_data:
                course = fetch_data.get_course(sql.cursor, code=course_code)
                course_data[course_code] = {
                    "name": course["name"],
                    "faculties": set(),
                    "hrs": 0
                }

            course_data[course_code]["faculties"].add(f"{faculty_name}({row['faculty_id']})")

        course_slots = {}
        for row in _timetables:
            code = row["course_code"]
            if code not in course_slots:
                course_slots[code] = set()
            course_slots[code].add((row["day"], row["period_id"]))

        for code, slots in course_slots.items():
            if code in course_data:
                course_data[code]["hrs"] = len(slots)

        for course in course_data.values():
            course["faculties"] = ", ".join(course["faculties"])

        return render_template("./timetable.html", days=DAYS, periods=periods,
                               grid=grid, course_data=course_data, title=title)
    return render_template("./failed.html", reason="Unknown error occurred")


@app.route("/update_timetable", methods=["GET", "POST"])
def update_timetable():
    assert sql.cursor

    campuses = show_data.get_campuses(sql.cursor)
    degrees = [s["name"] for s in show_data.get_degrees(sql.cursor)]
    streams = list({s["name"] for s in show_data.get_streams(sql.cursor)}) + [""]
    years = range(1, 11)
    sections = ["A", "B", "C", "D", "E"]

    campus = request.args.get("campus")
    degree = request.args.get("degree")
    stream = request.args.get("stream")
    year = request.args.get("year", type=int)
    section = request.args.get("section")

    current_timetables = []
    grid = {}
    section_id = None
    campus_id = show_data.get_campus_id(sql.cursor, campus=campus) if campus else None

    if all([campus_id, degree, year, section]) and (stream is not None):
        section_id = fetch_data.get_section_id(
            sql.cursor, campus_id=campus_id, degree=degree,
            stream=stream, year=year, section=section
        )

        if section_id:
            periods = fetch_data.get_periods(sql.cursor)
            grid = {day: {period["id"]: [] for period in periods} for day in DAYS}

            current_timetables = fetch_data.get_timetables(sql.cursor, section_id=section_id)
            
            for row in current_timetables:
                day = row["day"]
                period_id = row["period_id"]
                
                entry_data = {
                    "text": f"{row['course_code']} - {row['faculty_id']} ({row['room_no']})",
                    "is_lab": row["is_lab"],
                    "course_code": row["course_code"],
                    "faculty_id": row["faculty_id"]
                }
                if row["is_lab"]:
                    entry_data["text"] += " (Lab)"
                
                if day in grid and period_id in grid[day]:
                    grid[day][period_id].append(entry_data)

    return render_template(
        "update_timetable.html",
        campuses=campuses, degrees=degrees, streams=streams,
        years=years, sections=sections, timetables=current_timetables,
        grid=grid, section_id=section_id,
        campus_id=campus_id, campus=campus, degree=degree,
        stream=stream, year=year, section=section
    )


@app.route("/add_timetable_entry", methods=["POST"])
def add_timetable_entry():
    data = request.json
    assert sql.db_connector and sql.cursor and data is not None

    faculty_id = data.get("faculty_id")
    section_id = data.get("section_id")
    course_code = data.get("course_code")
    day = data.get("day")
    period = data.get("period")
    
    class_id = data.get("class_id")
    hrs = data.get("hrs")
    
    cursor = sql.cursor
    cursor.execute("""
        SELECT id FROM faculty_section_course 
        WHERE faculty_id=%s AND section_id=%s AND course_code=%s
    """, (faculty_id, section_id, course_code))
    
    existing_relations = cursor.fetchall()
    fsc_id = None

    if existing_relations:
        fsc_id = existing_relations[0]["id"]
    else:
        if not hrs or not class_id:
            return {"success": False, "message": "New mapping! Please provide Hours and Class ID."}
            
        insert_data.add_faculty_section_course(
            sql.db_connector, cursor,
            faculty_id=faculty_id, section_id=section_id, course_code=course_code,
            course="Unknown Course",
            hours=hrs, class_id=class_id,
            is_lab=data.get("is_lab", 0),
            is_elective=data.get("is_elective", 0),
            full_batch=data.get("full_batch", 1)
        )
        fsc_id = cursor.lastrowid

    try:
        cursor.execute("""
            INSERT IGNORE INTO timetables (day, period_id, faculty_section_course_id)
            VALUES (%s, %s, %s)
        """, (day, period, fsc_id))
        sql.db_connector.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/delete_timetable_entry", methods=["POST"])
def delete_timetable_entry():
    data = request.json
    assert sql.db_connector and sql.cursor and data is not None

    faculty_id = data["faculty_id"]
    section_id = data["section_id"]
    course_code = data["course_code"]
    day = data["day"]
    period = data["period"]

    try:
        cursor = sql.cursor
        cursor.execute("""
            SELECT id FROM faculty_section_course 
            WHERE faculty_id=%s AND section_id=%s AND course_code=%s
        """, (faculty_id, section_id, course_code))
        
        relations = cursor.fetchall()
        
        if not relations:
            return {"success": False, "message": "Entry not found"}
        
        for rel in relations:
            cursor.execute("""
                DELETE FROM timetables 
                WHERE day=%s AND period_id=%s AND faculty_section_course_id=%s
            """, (day, period, rel["id"]))
        
        sql.db_connector.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/logout")
def logout() -> Response:
    session.clear()
    sql.close()
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error: NotFound) -> tuple[str, int]:
    return (render_template("./404.html"), 404)


if __name__ == "__main__":
    app.config.update(
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True
    )
    app.run(host="0.0.0.0", port=5000, debug=False)
