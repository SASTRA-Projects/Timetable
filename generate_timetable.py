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


from collections import defaultdict
from itertools import combinations
from typehints import Connection, Cursor, Optional, Tuple
import fetch_data
import insert_data
import random
import show_data


def generate_timetable(db_connector: Connection, cursor: Cursor,
                       campus_id: Optional[int] = None,
                       days: tuple[str] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
                       period_ids: tuple[int] = tuple(range(1, 9))) -> None:

    PERIODS = {(day, period_id) for day in days for period_id in period_ids}

    def get_free_classes(no_of_students: int,
                         day: str,
                         period_id: int,
                         section_id: Optional[int] = None,
                         excl_cls: set[int] = set()) -> list[dict[str, bool | bool]]:
        section_floor = None
        section_class_id = None

        if section_id:
            cursor.execute("""SELECT `class_id`, `floor`
                           FROM `section_class`
                           JOIN `classes`
                           ON `classes`.`id`=`section_class`.`class_id`
                           WHERE `section_id`=%s
                           LIMIT 1""", (section_id,))
            section_class_info = cursor.fetchone()
            if section_class_info:
                section_class_id = section_class_info["class_id"]
                section_floor = section_class_info["floor"]

        print(section_class_id if section_class_id else -1,
                        campus_id, day, period_id,
                        section_id if section_id else -1,
                        no_of_students, day, period_id,
                        section_floor if section_floor else -1)
        cursor.execute("""SELECT DISTINCT(`classes`.`id`) AS `id`,
                       `classes`.`floor` AS `floor`,
                       `classes`.`room_no` AS `room_no`,
                       `classes`.`capacity` AS `capacity`,
                       `classes`.`department` AS `department`,
                       CASE 
                           WHEN `classes`.`id`=%s THEN 1
                           ELSE 0 
                       END AS `is_home_class`,
                       CASE 
                           WHEN `section_other_classes`.`class_id` IS NOT NULL THEN 1
                           ELSE 0
                       END AS `section_has_class_here`
                       FROM `classes`
                       JOIN `campus_buildings` `CB`
                       ON `CB`.`building_id` = `classes`.`building_id`
                       AND `CB`.`campus_id`=%s
                       LEFT JOIN (
                       SELECT DISTINCT `FSC`.`class_id`
                       FROM `timetables` `TT`
                       JOIN `faculty_section_course` `FSC`
                           ON `TT`.`faculty_section_course_id` = `FSC`.`id`
                       WHERE `TT`.`day`=%s
                           AND `TT`.`period_id`=%s
                           AND `FSC`.`section_id`=%s
                           AND `FSC`.`class_id` IS NOT NULL
                       ) AS `section_other_classes`
                       ON `section_other_classes`.`class_id` = `classes`.`id`
                       WHERE `classes`.`capacity` >= %s
                       AND `classes`.`is_lab` = 0
                       AND `classes`.`id` NOT IN (
                           SELECT DISTINCT `FSC`.`class_id`
                           FROM `timetables` `TT`
                           JOIN `faculty_section_course` `FSC`
                               ON `TT`.`faculty_section_course_id` = `FSC`.`id`
                           WHERE `TT`.`day`=%s
                               AND `TT`.`period_id`=%s
                               AND `FSC`.`class_id` IS NOT NULL
                       )
                       ORDER BY
                       `is_home_class` DESC,
                       CASE WHEN `classes`.`floor`=%s THEN 0 ELSE 1 END,
                       `section_has_class_here` DESC,
                       `classes`.`floor`,
                       `classes`.`capacity`,
                       `classes`.`room_no`""",
                       (section_class_id if section_class_id else -1,
                        campus_id, day, period_id,
                        section_id if section_id else -1,
                        no_of_students, day, period_id,
                        section_floor if section_floor else -1))
        return [r["id"] for r in cursor.fetchall() if r["id"] not in excl_cls]

    def get_free_periods(section_id):
        cursor.execute("""SELECT `day`, `period_id`
                       FROM `timetables`
                       JOIN `faculty_section_course` `FSC`
                       ON `FSC`.`id`=`faculty_section_course_id`
                       AND `section_id`=%s""", (section_id,))
        day_periods = {(dp["day"], dp["period_id"]) for dp in cursor.fetchall()}
        return PERIODS - day_periods

    def get_faculty_free_periods(faculty_id):
        cursor.execute("""SELECT `day`, `period_id`
                       FROM `timetables`
                       JOIN `faculty_section_course` `FSC`
                       ON `FSC`.`id`=`faculty_section_course_id`
                       AND `faculty_id`=%s""", (faculty_id,))
        day_periods = {(dp["day"], dp["period_id"]) for dp in cursor.fetchall()}
        return PERIODS - day_periods

    def get_cls_idx(day_period):
        def dpsort(dp):
            p = dp[1] - 5 if dp[1] > 4 else 4 - dp[1]
            return (p, -days[dp[0]], random.random() >= 0.5)

        days = {}
        for d, p in day_period:
            days[d] = days.get(d, 0) + 1

        _day_period = day_period.copy()
        while _day_period:
            _day_period = sorted(_day_period, key=dpsort)
            day, p = _day_period.pop(0)
            idx = day_period.index((day, p))
            yield idx
            days[day] -= 1
            if days[day] == 0:
                del days[day]

    def cls_capacities(day, period_id, class_id=None):
        if class_id:
            cursor.execute("""SELECT MAX(`strength`) AS `strength`,
                           `course_code`, `FSC`.`section_id`,
                           (2-MIN(`full_batch`)) AS `no_of_batch`
                           FROM `timetables`
                           JOIN `faculty_section_course` `FSC`
                           ON `faculty_section_course_id`=`FSC`.`id`
                           JOIN `section_class` `SC`
                           ON `FSC`.`section_id`=`SC`.`section_id`
                           AND `FSC`.`class_id`=%s
                           AND `day`=%s
                           AND `period_id`=%s
                           AND NOT `is_elective`
                           GROUP BY `course_code`, `FSC`.`section_id`""",
                           (class_id, day, period_id))
            lab_students = tuple({
                "strength": f["strength"],
                "no_of_batch": f["no_of_batch"]
            } for f in cursor.fetchall())

            cursor.execute("""SELECT COUNT(*) AS `strength`, `FSC`.`course_code`,
                           (2-MIN(`full_batch`)) AS `no_of_batch`
                           FROM `timetables`
                           JOIN `faculty_section_course` `FSC`
                           ON `faculty_section_course_id`=`FSC`.`id`
                           AND `is_elective`
                           JOIN `student_electives` `SS`
                           ON `SS`.`course_code`=`FSC`.`course_code`
                           AND `class_id`=%s
                           AND `day`=%s
                           AND `period_id`=%s
                           GROUP BY `FSC`.`course_code`""", (class_id, day, period_id))
            elective_lab_students = tuple({
                "strength": f["strength"],
                "no_of_batch": f["no_of_batch"]
            } for f in cursor.fetchall() if f["strength"] > 0)


            cursor.execute("""SELECT `capacity`
                           FROM `classes`
                           WHERE `id`=%s""", (class_id,))
            capacity = cursor.fetchone()["capacity"]

            return capacity - sum(s["strength"]//s["no_of_batch"]
                                  for s in lab_students + elective_lab_students)
        return None

    def max_cls_capacity(day, period_id, class_id=None, no_of_students=0):
        class_capacity = cls_capacities(day, period_id, class_id)
        if class_id:
            return class_capacity if class_capacity >= no_of_students else 0

        return sorted(filter(lambda x: x[1] >= no_of_students, class_capacity),
                      key=lambda x: x[1], reverse=True)

    def schedule_electives(student_choices, electives: dict[str, int | None]) -> dict[int, set[str]]:
        conflict_graph = defaultdict(set)
        for choices in student_choices:
            for c1, c2 in combinations(choices, 2):
                conflict_graph[c1].add(c2)
                conflict_graph[c2].add(c1)

        all_courses = list(electives.keys())
        for c1, c2 in combinations(all_courses, 2):
            class_id_1 = electives.get(c1)
            class_id_2 = electives.get(c2)
            if class_id_1 is not None and class_id_1 == class_id_2:
                conflict_graph[c1].add(c2)
                conflict_graph[c2].add(c1)

        sorted_courses = sorted(all_courses, key=lambda x: len(conflict_graph[x]), reverse=True)
        course_slots: dict[str, int] = {}
        for course in sorted_courses:
            neighbor_slots = {
                course_slots[neighbor]
                for neighbor in conflict_graph[course]
                if neighbor in course_slots
            }
            slot = 0
            while slot in neighbor_slots:
                slot += 1
            course_slots[course] = slot

        schedule_output = defaultdict(set)
        for course, slot in course_slots.items():
            schedule_output[slot].add(course)

        return dict(schedule_output)


    def update_fsc(f_id, cls_id):
        cursor.execute("""UPDATE `faculty_section_course`
                       SET `class_id`=%s
                       WHERE `id`=%s""", (cls_id, f_id))
        db_connector.commit()

    def add_timetable(f_id, day, period_id):
        insert_data.add_timetable(cursor, day=day, period_id=period_id, faculty_section_course_id=f_id)

    def delete_timetable(f_id, day, period_id):
        cursor.execute("""DELETE FROM `timetables`
                       WHERE `faculty_section_course_id`=%s
                       AND `day`=%s
                       AND `period_id`=%s""", (f_id, day, period_id))
        db_connector.commit()

    def elective_labs(fsc, std_electives, periods) -> dict[str, set[tuple[str, int]]]:
        elective_hrs: dict[str, set[tuple[str, int]]] = {}
        tot_std: dict[str, int] = {}

        courses = {_f["course_code"] for _f in fsc}
        for _f in fsc:
            batch = (2 - _f["full_batch"])
            num = len({s for s, e in std_electives.items() if e in courses})
            tot_std[_f["course_code"]] = num // batch
            for _p in periods.copy():
                if not max_cls_capacity(*_p, class_id=_f["class_id"], no_of_students=num//batch):
                    periods -= {_p, (_p[0], _p[1]+1)}

        periods = list(periods)
        cls_idx = get_cls_idx(periods)
        while fsc:
            try:
                _cls_idx = next(cls_idx)
                p = periods[_cls_idx]
                _timetable = []
                for _f in fsc:
                    batch = (2 - _f["full_batch"])
                    if _f["hrs"] < 0:
                        print(_f, 370)

                    if not max_cls_capacity(
                        p[0], p[1], class_id=_f["class_id"],
                        no_of_students=tot_std[_f["course_code"]]//batch
                    ):
                        periods.remove(p)
                        cls_idx = get_cls_idx(periods)
                        print(f"Lab's full {_f["class_id"]}")
                        raise ValueError(f"Lab's full {_f["class_id"]} {_f["course_code"]}")
                    _timetable.append((_f, *p))

                _elective_hrs: dict[str, set[tuple[str, int]]] = defaultdict(set)
                for t in _timetable:
                    _f = t[0]
                    add_timetable(_f["id"], t[1], t[2])
                    add_timetable(_f["id"], t[1], t[2] + 1)
                    _elective_hrs[_f["course_code"]] |= {t[1:], (t[1], t[2]+1)}
                elective_hrs.update(_elective_hrs)

                to_remove = []
                for _f in fsc:
                    _f["hrs"] -= 2
                    if _f["hrs"] == 0:
                        to_remove.append(_f)
                for t in to_remove:
                    fsc.remove(t)

                print(courses, p)
                periods.remove(p)
                db_connector.commit()

            except Exception as e:
                _exception = e.args
                print(_exception, p)
                db_connector.rollback()
                if len(_exception) < 2:
                    if len(periods) > 0:
                        try:
                            next(cls_idx)
                        except:
                            print("cls_idx over\n")
                            cls_idx = get_cls_idx(periods)
                            if len(_exception) and 'out of range' in _exception[0]:
                                cls_idx = get_cls_idx(periods)
                        print(380, _exception, periods, p, _cls_idx)
                        continue
                    print(_exception, 11, "Over")
                    return {}

                if "Non-lab classes" in _exception[1] or "Duplicate" in _exception[1]:
                    periods.remove(p)
                    cls_idx = get_cls_idx(periods)

                elif "same day" in _exception[1] or "same time" in _exception[1]:
                    day = periods[_cls_idx][0]
                    for d, p in periods:
                        if d == day:
                            periods.remove((d, p))
                    cls_idx = get_cls_idx(periods)

                elif "faculty" in _exception[1] or "more than 2 labs at same time" in _exception[1]:
                    periods.remove(p)
                    cls_idx = get_cls_idx(periods)

                elif "lunch" in _exception[1]:
                    periods.pop(_cls_idx)
                    cls_idx = get_cls_idx(periods)

                if not (_cls_idx >= 0 and len(periods) <= _cls_idx + 1):
                    cls_idx = get_cls_idx(periods)
        return elective_hrs

    # 1. Allocate elective labs, then theory
    sec_map = {int(s["id"]): (s["degree"], s["stream"], s["year"], s["section"])
               for s in fetch_data.get_sections(cursor, campus_id=campus_id)}
    degrees = show_data.get_degrees(cursor)
    for _degree in degrees:
        degree = _degree["name"]
        fsc = fetch_data.get_electives(cursor, degree=degree)
        yr_electives = defaultdict(lambda: defaultdict(set))
        std_electives = defaultdict(set)
        yr_students = defaultdict(set)
        _sec_electives = defaultdict(set)
        for f in fsc:
            if f["course_code"] not in std_electives:
                assert isinstance(f["section_id"], int) and isinstance(f["course_code"], str)
                section = fetch_data.get_section(cursor, section_id=f["section_id"])

                assert section is not None and isinstance(section["year"], int)
                year = section["year"]

                assert isinstance(year, int)
                yr_electives[year][f["course_code"]].add(f["class_id"])
                _sec_electives[sec_map[f["section_id"]]].add(f["course_code"])

                for s in fetch_data.get_student_electives(cursor, course_code=f["course_code"]):
                    std_electives[s["student_id"]].add(f["course_code"])
                    yr_students[year].add(s["student_id"])

        if not yr_electives:
            continue

        for year, _electives in yr_electives.items():
            student_choices = set()
            for s_id in yr_students[year]:
                student_choices.add(tuple(std_electives[s_id]))

            _electives = schedule_electives(student_choices, _electives).values()
            electives: list[set[str]] = []
            for s in _electives:
                overlap = [c for c in electives if not s.isdisjoint(c)]
                rest = [c for c in electives if s.isdisjoint(c)]
                combined = s.union(*overlap)
                electives = [combined] + rest

            for _courses in electives:
                    _periods = PERIODS
                    _fsc = list(filter(lambda x: x["course_code"] in _courses, fsc))

                    tot_std: dict[str, int] = {}
                    _lab_hrs = [_f for _f in _fsc if _f["is_lab"]]
                    _lab_fac_period = PERIODS
                    _fac_period = PERIODS
                    _sec_period = PERIODS
                    for _f in _fsc:
                        if _f["is_lab"]:
                            _lab_fac_period &= get_faculty_free_periods(_f["faculty_id"])
                        else:
                            _fac_period &= get_faculty_free_periods(_f["faculty_id"])
                        _sec_period &= get_free_periods(section_id=_f["section_id"])

                    _periods &= _sec_period
                    lab_hrs: dict[str, set[tuple[str, int]]] = {}
                    if _lab_hrs:
                        lab_hrs = elective_labs(_lab_hrs, std_electives,
                                                {_p for _p in _periods & _lab_fac_period if _p[1] % 2})
                        assert lab_hrs

                    _fsc = [_f for _f in _fsc if not _f["is_lab"]]
                    _periods = {_p for _p in _periods if _p[1] != 5}
                    _excl_cls = set()
                    for _f in _fsc:
                        if _f["class_id"] is None:
                            num = len({s for s, e in std_electives.items() if e in _courses})
                            tot_std[_f["course_code"]] = num
                        else:
                            _excl_cls.add(_f["class_id"])

                    _periods -= {(d, 5) for d in days}
                    periods = list(_periods & _fac_period)
                    cls_idx = get_cls_idx(periods)
                    _no_error = True
                    _stsl = False
                    while _fsc:
                        try:
                            _p = set(periods)
                            __fsc = filter(lambda x: x["course_code"] not in _courses, fsc)
                            for _f in __fsc:
                                _p &= (PERIODS - get_free_periods(_f["faculty_id"]))
                            if _p:
                                cls_idx = get_cls_idx(list(_p))
                            _cls_idx = next(cls_idx)
                            p = periods[_cls_idx]
                            k = 0
                            while _stsl and any(lab_hrs.get(c) == p for c in _courses):
                                _cls_idx = next(cls_idx)
                                p = periods[_cls_idx]

                            classes = get_free_classes(60, p[0], p[1], _fsc[0]["section_id"], _excl_cls)
                            _timetable = []
                            for _f in _fsc:
                                if _f["class_id"] is None and _no_error:
                                    if tot_std[_f["course_code"]] > 60:
                                        cls_id = get_free_classes(tot_std[_f["course_code"]], *p, _f["section_id"], _excl_cls)[0]
                                        update_fsc(_f["id"], cls_id)
                                    else:
                                        update_fsc(_f["id"], classes[k])
                                        k = (k + 1) % len(classes)
                                if not _stsl and _f["course_code"] in lab_hrs \
                                and p in lab_hrs[_f["course_code"]]:
                                    _stsl = True
                                else:
                                    _timetable.append((_f, *p))

                            for t in _timetable:
                                add_timetable(t[0]["id"], t[1], t[2])

                            to_remove = []
                            for _f in _fsc:
                                if _f["course_code"] not in lab_hrs \
                                    or lab_hrs and p not in lab_hrs[_f["course_code"]]:
                                    _f["hrs"] -= 1
                                if _f["hrs"] == 0:
                                    to_remove.append(_f)

                            for t in to_remove:
                                _fsc.remove(t)

                            print(_courses, sec_map[_f["section_id"]], p)
                            periods.remove(p)
                            _no_error = False
                            db_connector.commit()

                        except Exception as e:
                            _exception = e.args
                            print(_exception, p)
                            db_connector.rollback()
                            if len(_exception) < 2:
                                if len(periods) > 0:
                                    try:
                                        next(cls_idx)
                                    except:
                                        print("cls_idx over\n")
                                        cls_idx = get_cls_idx(periods)
                                    if len(_exception) and 'out of range' in _exception[0]:
                                        cls_idx = get_cls_idx(periods)
                                    print(550, _exception, periods, p, _cls_idx)
                                    continue
                                print(_exception, 12, "Over")
                                return None

                            if "Non-lab classes" in _exception[1] or "Duplicate" in _exception[1]:
                                if any(_f["class_id"] for _f in _fsc):
                                    periods.remove(p)
                                    cls_idx = get_cls_idx(periods)
                            elif "same day" in _exception[1] or "same time" in _exception[1]:
                                day = periods[_cls_idx][0]
                                for d, p in periods:
                                    if d == day:
                                        periods.remove((d, p))
                                cls_idx = get_cls_idx(periods)

                            elif "faculty" in _exception[1] or "more than 2 labs at same time" in _exception[1]:
                                periods.remove(p)
                                cls_idx = get_cls_idx(periods)

                            elif "lunch" in _exception[1]:
                                periods.pop(_cls_idx)
                                cls_idx = get_cls_idx(periods)

                            if not (_cls_idx >= 0 and len(periods) <= _cls_idx + 1):
                                cls_idx = get_cls_idx(periods)
                            for _f in _fsc:
                                if _f["class_id"] is None:
                                    update_fsc(_f["id"], None)

    # 2. Allocate non-elective lab courses
    # for section_id in sec_map:
    #     __fsc = fetch_data.get_faculty_section_courses(cursor, section_id=section_id, is_elective=False, is_lab=True)
    #     fsc = defaultdict(list)
    #     num = fetch_data.get_section(cursor, section_id=section_id)["strength"]
    #     for _f in __fsc:
    #         fsc[str(_f["course_code"])].append(_f)

    #     processed_ids = set()
    #     paired_groups = {}
    #     solo_courses = set()
    #     first_allocation_done = set()
    #     for course_code in fsc:
    #         if course_code=="CAP209":
    #             print(end="")

    #         while True:
    #             rows = [r for r in fsc[course_code] if r["id"] not in processed_ids and r["hrs"] > 0]
    #             if not rows: 
    #                 break

    #             rows = [r for r in rows if r["class_id"] != 619]
    #             if not rows: 
    #                 break

    #             rows.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))
    #             is_split = not rows[0]["full_batch"]
    #             _periods_base = get_free_periods(section_id=section_id) & PERIODS
    #             if course_code in paired_groups:
    #                 paired_course = paired_groups[course_code]
    #                 primary_rows = rows
    #                 paired_rows = [r for r in fsc[paired_course] if r["id"] not in processed_ids and r["hrs"] > 0 and r["class_id"] != 619]
    #                 if not paired_rows:
    #                     del paired_groups[course_code]
    #                     if paired_course in paired_groups:
    #                         del paired_groups[paired_course]
    #                     solo_courses.add(course_code)
    #                     _fsc = primary_rows
    #                     strategy = [(_fsc, None)]

    #                 else:
    #                     paired_rows.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))
    #                     _fsc = primary_rows + paired_rows
    #                     strategy = [(_fsc, paired_course)]

    #             elif course_code in solo_courses:
    #                 _fsc = rows
    #                 strategy = [(_fsc, None)]

    #             else:
    #                 if len(rows) > 2 and course_code not in ("CHY101", "CIV103"):
    #                     _fsc = rows[:(len(rows)+1)//2]
    #                 else:
    #                     _fsc = rows

    #                 strategy = []
    #                 if is_split:
    #                     primary_ids = {x["faculty_id"] for x in _fsc}
    #                     prim_periods = _periods_base.copy()
    #                     for _f in _fsc: 
    #                         prim_periods &= get_faculty_free_periods(_f["faculty_id"])

    #                     potential_pairs = []
    #                     for other_code in fsc:
    #                         if other_code == course_code: 
    #                             continue
    #                         if other_code in paired_groups or other_code in solo_courses:
    #                             continue

    #                         others = [r for r in fsc[other_code] if r["id"] not in processed_ids and r["hrs"] > 0 and r["class_id"] != 619]
    #                         if not others: 
    #                             continue

    #                         other_is_split = not others[0]["full_batch"] or (others[0]["hrs"] > 2 and other_code not in first_allocation_done)
    #                         if not other_is_split:
    #                             continue

    #                         if not primary_ids.isdisjoint({x["faculty_id"] for x in others}): 
    #                             continue

    #                         others.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))                            
    #                         if len(others) > 2:
    #                             cand = others[:(len(others)+1)//2]
    #                         else:
    #                             cand = others[:]

    #                         tmp = prim_periods.copy()
    #                         for _f in cand: 
    #                             tmp &= get_faculty_free_periods(_f["faculty_id"])

    #                         overlap_len = len(tmp)
    #                         if overlap_len > 0:
    #                             potential_pairs.append((overlap_len, other_code, cand))

    #                     potential_pairs.sort(key=lambda x: x[0], reverse=True)
    #                     for _, other_code, pair in potential_pairs:
    #                         strategy.append((_fsc + pair, other_code))

    #                 strategy.append((_fsc, None))

    #             allocated_chunk = False
    #             for strategy_fsc, paired_with in strategy:
    #                 _periods = _periods_base.copy()
    #                 for _f in strategy_fsc: 
    #                     _periods &= get_faculty_free_periods(_f["faculty_id"])

    #                 periods = list(_p for _p in _periods if _p[1] % 2 != 0 and (_p[0], _p[1]+1) in _periods)
    #                 if not periods: 
    #                     continue

    #                 cls_idx = get_cls_idx(periods)
    #                 strategy_success = False                    
    #                 while True:
    #                     try:
    #                         try:
    #                             _idx = next(cls_idx)
    #                         except StopIteration:
    #                             if len(periods) > 0:
    #                                 cls_idx = get_cls_idx(periods, section_id)
    #                                 continue
    #                             break

    #                         p = periods[_idx]
    #                         _timetable = []
    #                         for _f in strategy_fsc:
    #                             batch = 2 - _f["full_batch"]
    #                             if not max_cls_capacity(p[0], p[1], class_id=_f["class_id"], no_of_students=num//batch):
    #                                 raise ValueError(f"Lab's full {_f['class_id']}")
    #                             _timetable.append((_f, *p))

    #                         for t in _timetable:
    #                             add_timetable(t[0]["id"], t[1], t[2])
    #                             add_timetable(t[0]["id"], t[1], t[2]+1)

    #                         db_connector.commit()
    #                         for t in _timetable:
    #                             t[0]["hrs"] -= 2

    #                         if course_code not in first_allocation_done:
    #                             first_allocation_done.add(course_code)                                
    #                             if paired_with:
    #                                 paired_groups[course_code] = paired_with
    #                                 paired_groups[paired_with] = course_code
    #                                 first_allocation_done.add(paired_with)
    #                                 print(f"{p} {section_id} Success - PAIRED: {course_code} <-> {paired_with}")
    #                             else:
    #                                 solo_courses.add(course_code)
    #                                 print(f"{p} {section_id} Success - SOLO: {course_code}")
    #                         else:
    #                             if course_code in paired_groups:
    #                                 print(f"{p} {section_id} Success - {course_code} (with {paired_groups[course_code]})")
    #                             else:
    #                                 print(f"{p} {section_id} Success - {course_code} (solo)")

    #                         processed_ids.update(x["id"] for x in strategy_fsc if x["hrs"] <= 0)
    #                         strategy_success = True
    #                         break

    #                     except Exception as e:
    #                         db_connector.rollback()
    #                         ex = e.args
    #                         print(ex)
    #                         if len(ex) < 2 or "Lab's full" in str(ex):
    #                             if p in periods: 
    #                                 periods.remove(p)
    #                             cls_idx = get_cls_idx(periods)
    #                         elif "faculty" in str(ex) or "same" in str(ex) or "Duplicate" in str(ex):
    #                             if p in periods: 
    #                                 periods.remove(p)
    #                             cls_idx = get_cls_idx(periods)
    #                         elif "lunch" in str(ex):
    #                             if _idx < len(periods): 
    #                                 periods.pop(_idx)
    #                             cls_idx = get_cls_idx(periods)
    #                         else:
    #                             if p in periods: 
    #                                 periods.remove(p)
    #                             cls_idx = get_cls_idx(periods)

    #                 if strategy_success:
    #                     allocated_chunk = True
    #                     break

    #             if not allocated_chunk:
    #                 print(f"Failed to allocate {section_id} {course_code} Hrs: {rows[0]['hrs']}")
    #                 return None

    # ==========================================
    # HELPER FUNCTIONS & SWAPPING LOGIC
    # ==========================================

    def max_cls_capacity(day, period_id, class_id, no_of_students):
        """Checks if room has space for new students."""
        if not class_id: return True # Virtual room
        cursor.execute("SELECT `capacity` FROM `classes` WHERE `id`=%s", (class_id,))
        res = cursor.fetchone()
        if not res: return True 
        
        # Calculate Current Occupancy
        # Get all sections currently in this class at this time
        cursor.execute("""
            SELECT DISTINCT `FSC`.`section_id`, `FSC`.`full_batch`
            FROM `timetables` `T`
            JOIN `faculty_section_course` `FSC` ON `T`.`faculty_section_course_id`=`FSC`.`id`
            WHERE `T`.`day`=%s AND `T`.`period_id`=%s AND `FSC`.`class_id`=%s
        """, (day, period_id, class_id))
        
        current_occupancy = 0
        rows = cursor.fetchall()
        for r in rows:
            # Fetch strength from section_class
            # We use LIMIT 1 assuming strength is consistent for the section
            cursor.execute("SELECT `strength` FROM `section_class` WHERE `section_id`=%s LIMIT 1", (r['section_id'],))
            s_res = cursor.fetchone()
            if s_res:
                strength = s_res['strength']
                current_occupancy += strength if r['full_batch'] else (strength // 2)
            
        return (current_occupancy + no_of_students) <= res['capacity']

    def delete_timetable_safe(fsc_id, day, period_id):
        cursor.execute("DELETE FROM `timetables` WHERE `faculty_section_course_id`=%s AND `day`=%s AND `period_id`=%s", (fsc_id, day, period_id))

    def add_timetable_safe(fsc_id, day, period_id):
        insert_data.add_timetable(cursor, day=day, period_id=period_id, faculty_section_course_id=fsc_id)

    def resolve_conflict_recursive(target_fsc_list, section_id, duration, depth=0, forbidden=None):
        """
        Attempts to make space for a list of FSCs (strategy) by moving blockers.
        target_fsc_list: list of FSC dicts to allocate together.
        section_id: The section_id of the target courses (passed explicitly).
        duration: 2 for labs, 1 for theory.
        """
        if depth > 1: return False
        if forbidden is None: forbidden = set()

        candidates = list(PERIODS)
        random.shuffle(candidates)

        for day, period in candidates:
            if period == 5: continue
            
            slots = [period]
            if duration == 2:
                if period not in (1, 3, 6, 7): continue
                if (day, period+1) not in PERIODS: continue
                if period == 4: continue
                slots = [period, period+1]

            if any((day, p) in forbidden for p in slots): continue

            # Check Capacity (HARD Constraint)
            cap_ok = True
            # Fetch strength for the target section once
            try:
                sec_classes = fetch_data.get_section_classes(cursor, section_id=section_id)
                if not sec_classes: raise ValueError("No section class info")
                str_val = sec_classes[0]['strength']
            except:
                # Fallback if fetch_data fails or returns empty
                cursor.execute("SELECT strength FROM section_class WHERE section_id=%s LIMIT 1", (section_id,))
                res = cursor.fetchone()
                str_val = res['strength'] if res else 60 # Default fallback

            for fsc in target_fsc_list:
                needed = str_val if fsc['full_batch'] else (str_val // 2)
                for p in slots:
                    if not max_cls_capacity(day, p, fsc['class_id'], needed):
                        cap_ok = False; break
                if not cap_ok: break
            if not cap_ok: continue

            # Identify Blockers
            blockers = set()
            
            # Faculty Blockers
            for fsc in target_fsc_list:
                for p in slots:
                    cursor.execute("""SELECT `faculty_section_course_id` FROM `timetables` 
                                      JOIN `faculty_section_course` `F` ON `F`.`id`=`faculty_section_course_id`
                                      WHERE `day`=%s AND `period_id`=%s AND `faculty_id`=%s""", 
                                      (day, p, fsc['faculty_id']))
                    blockers.update(r['faculty_section_course_id'] for r in cursor.fetchall())
            
            # Section Blockers
            for p in slots:
                cursor.execute("""SELECT `faculty_section_course_id` FROM `timetables` 
                                  JOIN `faculty_section_course` `F` ON `F`.`id`=`faculty_section_course_id`
                                  WHERE `day`=%s AND `period_id`=%s AND `section_id`=%s""", 
                                  (day, p, section_id))
                blockers.update(r['faculty_section_course_id'] for r in cursor.fetchall())

            target_ids = {f['id'] for f in target_fsc_list}
            blockers = list(blockers - target_ids)

            max_blockers = 3 + depth  # Allow more blockers at deeper recursion levels
            if blockers and len(blockers) > max_blockers:
                continue

            sp_name = f"swap_{depth}_{random.randint(1000,9999)}"
            try:
                cursor.execute(f"SAVEPOINT {sp_name}")
                
                # 1. Delete Blockers
                moved_blockers = []
                for b_id in blockers:
                    # Fetch full FSC info for blocker to get its section_id
                    b_info = fetch_data.get_faculty_section_course(cursor, faculty_section_course_id=b_id)
                    if not b_info: raise Exception("Invalid blocker")

                    b_slots = fetch_data.get_timetables(cursor, faculty_section_course_id=b_id)
                    for bs in b_slots:
                        delete_timetable_safe(b_id, bs['day'], bs['period_id'])

                    moved_blockers.append((b_info, b_slots))
                
                # 2. Insert Target
                for fsc in target_fsc_list:
                    for p in slots:
                        add_timetable_safe(fsc['id'], day, p)

                # 3. Re-allocate Blockers (Recursion)
                new_forbidden = forbidden.copy()
                for p in slots: new_forbidden.add((day, p))
                
                for b_info, old_slots in moved_blockers:
                    b_dur = 2 if b_info['is_lab'] else 1
                    # Pass the blocker's section_id explicitely
                    if not resolve_conflict_recursive([b_info], b_info['section_id'], b_dur, depth+1, new_forbidden):
                        raise Exception("Failed to re-allocate blocker")

                cursor.execute(f"RELEASE SAVEPOINT {sp_name}")
                print(f"      [Swap Success] Moved {len(moved_blockers)} blockers to fit {target_fsc_list[0]['course_code']}")
                return True

            except Exception:
                cursor.execute(f"ROLLBACK TO SAVEPOINT {sp_name}")
                continue
                
        return False

    # ==========================================
    # 2. ALLOCATE NON-ELECTIVE LABS
    # ==========================================
    print("\n=== Allocating Non-Elective Labs ===")
    
    for section_id in sec_map:
        __fsc = fetch_data.get_faculty_section_courses(cursor, section_id=section_id, is_elective=False, is_lab=True)
        fsc_map = defaultdict(list)
        
        # We need section strength. Fetching it safely.
        try:
            sec_classes = fetch_data.get_section_classes(cursor, section_id=section_id)
            if sec_classes:
                 section_strength = sec_classes[0]['strength']
            else:
                 # Fallback
                 cursor.execute("SELECT strength FROM section_class WHERE section_id=%s LIMIT 1", (section_id,))
                 res = cursor.fetchone()
                 section_strength = res['strength'] if res else 60
        except:
            section_strength = 60

        for _f in __fsc:
            fsc_map[str(_f["course_code"])].append(_f)
            
        processed_ids = set()
        paired_groups = {}
        solo_courses = set()
        first_allocation_done = set()
        
        keys = list(fsc_map.keys())

        for course_code in keys:
            while True:
                rows = [r for r in fsc_map[course_code] if r["id"] not in processed_ids and r["hrs"] > 0]
                rows = [r for r in rows if r["class_id"] != 619]
                if not rows:
                    break

                rows.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))
                is_split = not rows[0]["full_batch"]
                strategy = []
                if course_code in paired_groups:
                    partner = paired_groups[course_code]
                    p_rows = [r for r in fsc_map[partner] if r["id"] not in processed_ids and r["hrs"] > 0]
                    p_rows = [r for r in p_rows if r["class_id"] != 619]
                    
                    if p_rows:
                         p_rows.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))
                         strategy = [(rows + p_rows, partner)]
                    else:
                         strategy = [(rows, None)]
                elif course_code in solo_courses:
                    strategy = [(rows, None)]
                else:
                    current_batch = rows
                    if len(rows) > 2 and course_code not in ("CHY101", "CIV103"):
                        current_batch = rows[:(len(rows)+1)//2]
                    
                    if is_split:
                        primary_ids = {x["faculty_id"] for x in current_batch}
                        found_partner = False
                        for cand_code in fsc_map:
                            if cand_code == course_code or cand_code in paired_groups or cand_code in solo_courses: continue
                            cand_rows = [r for r in fsc_map[cand_code] if r["id"] not in processed_ids and r["hrs"] > 0]
                            cand_rows = [r for r in cand_rows if r["class_id"] != 619]
                            if not cand_rows: continue
                            
                            if cand_rows[0]['full_batch']: continue
                            
                            cand_fac = {x['faculty_id'] for x in cand_rows}
                            if not primary_ids.isdisjoint(cand_fac): continue
                            
                            cand_rows.sort(key=lambda x: (-int(x["hrs"]), x["course"], x["class_id"], x["faculty_id"]))
                            cand_slice = cand_rows
                            if len(cand_rows) > 2: cand_slice = cand_rows[:(len(cand_rows)+1)//2]
                            
                            strategy.append((current_batch + cand_slice, cand_code))
                            found_partner = True
                            break
                        
                        if not found_partner:
                            strategy.append((current_batch, None))
                    else:
                        strategy.append((rows, None))

                success = False
                for target_fscs, partner_code in strategy:
                    if resolve_conflict_recursive(target_fscs, section_id, duration=2):
                        db_connector.commit()
                        
                        for x in target_fscs: x['hrs'] -= 2
                        processed_ids.update(x['id'] for x in target_fscs if x['hrs'] <= 0)
                        
                        if course_code not in first_allocation_done:
                            first_allocation_done.add(course_code)
                            if partner_code:
                                paired_groups[course_code] = partner_code
                                paired_groups[partner_code] = course_code
                                first_allocation_done.add(partner_code)
                                print(f"  Allocated PAIRED: {course_code} & {partner_code}")
                            else:
                                solo_courses.add(course_code)
                                print(f"  Allocated SOLO: {course_code}")
                        
                        success = True
                        break
                
                if not success:
                    print(f"  FAILED to allocate Lab {course_code} (Section {section_id})")
                    break

    # ==========================================
    # 3. ALLOCATE NON-ELECTIVE THEORY
    # ==========================================
    print("\n=== Allocating Non-Elective Theory ===")
    
    for section_id in sec_map:
        theory_courses = list(fetch_data.get_faculty_section_courses(
            cursor, section_id=section_id, is_elective=False, is_lab=False
        ))
        theory_courses.sort(key=lambda x: x['hrs'], reverse=True)
        
        for course in theory_courses:
            while course["hrs"] > 0:
                allocated = False
                
                # 1. Try Direct Allocation (Fast)
                free_slots = list(get_free_periods(section_id) & get_faculty_free_periods(course['faculty_id']))
                random.shuffle(free_slots)
                
                for p in free_slots:
                    if p[1] == 5: continue
                    try:
                        add_timetable_safe(course["id"], p[0], p[1])
                        db_connector.commit()
                        course["hrs"] -= 1
                        allocated = True
                        break
                    except:
                        db_connector.rollback()
                        continue
                
                # 2. Try Swap (Smart)
                if not allocated:
                    # Pass section_id explicitely
                    if resolve_conflict_recursive([course], section_id, duration=1):
                        db_connector.commit()
                        course["hrs"] -= 1
                    else:
                        print(f"  FAILED Theory {course['course_code']} (Section {section_id})")
                        break

    # ==========================================
    # 4. GLOBAL CONSTRAINT SOLVER (The "Fixer")
    # ==========================================
    
    def get_conflicting_entries(day, period, faculty_id, section_id, class_id):
        """
        Finds ALL timetable entries that would prevent an allocation at (day, period).
        Returns a list of (timetable_id, fsc_id, reason).
        """
        conflicts = []
        
        # 1. Faculty Busy?
        cursor.execute("""
            SELECT `faculty_section_course_id` FROM `timetables`
            WHERE `day`=%s AND `period_id`=%s 
            AND `faculty_section_course_id` IN (
                SELECT `id` FROM `faculty_section_course` WHERE `faculty_id`=%s
            )
        """, (day, period, faculty_id))
        for row in cursor.fetchall():
            conflicts.append((row['faculty_section_course_id'], 'faculty'))

        # 2. Section Busy?
        cursor.execute("""
            SELECT `faculty_section_course_id` FROM `timetables`
            WHERE `day`=%s AND `period_id`=%s 
            AND `faculty_section_course_id` IN (
                SELECT `id` FROM `faculty_section_course` WHERE `section_id`=%s
            )
        """, (day, period, section_id))
        for row in cursor.fetchall():
            conflicts.append((row['faculty_section_course_id'], 'section'))

        # 3. Room Full? (Only if specific room assigned)
        if class_id:
            # Calculate current strength vs capacity
            cursor.execute("SELECT `capacity` FROM `classes` WHERE `id`=%s", (class_id,))
            res = cursor.fetchone()
            if res:
                capacity = res['capacity']
                cursor.execute("""
                    SELECT `T`.`faculty_section_course_id`, `S`.`strength`, `FSC`.`full_batch`
                    FROM `timetables` `T`
                    JOIN `faculty_section_course` `FSC` ON `T`.`faculty_section_course_id`=`FSC`.`id`
                    JOIN `section_class` `S` ON `FSC`.`section_id`=`S`.`section_id`
                    WHERE `T`.`day`=%s AND `T`.`period_id`=%s AND `FSC`.`class_id`=%s
                """, (day, period, class_id))
                
                occupants = cursor.fetchall()
                current_occ = sum(occ['strength'] if occ['full_batch'] else occ['strength']//2 for occ in occupants)
                
                # We need to know OUR strength to see if we fit
                my_sec_cls = fetch_data.get_section_classes(cursor, section_id=section_id)
                my_strength = my_sec_cls[0]['strength'] if my_sec_cls else 60
                
                if current_occ + my_strength > capacity:
                    # Logic: If full, we consider EVERYONE in the room as a potential conflict
                    # Removing one might be enough, but for simplicity, we list them all.
                    for occ in occupants:
                         conflicts.append((occ['faculty_section_course_id'], 'room'))

        return conflicts

    def solve_recursively(pending_courses, depth=0):
        """
        Enhanced Global DFS with Min-Conflicts Heuristic.
        Prioritizes slots that require the LEAST amount of displacement.
        """
        if not pending_courses:
            return True # All allocated!
        
        # 1. Sort Pending: Hardest First (Labs, then High Hours)
        pending_courses.sort(key=lambda x: (x['fsc']['is_lab'], x['hrs_needed']), reverse=True)
        
        current = pending_courses[0]
        fsc = current['fsc']
        hrs_needed = current['hrs_needed']
        
        if hrs_needed <= 0:
            return solve_recursively(pending_courses[1:], depth)
            
        if depth % 20 == 0:
             print(f"[{depth}] Fitting {fsc['course_code']} (Sec {fsc['section_id']})...")

        duration = 2 if fsc['is_lab'] else 1
        
        candidates = []
        all_periods = list(PERIODS)
        random.shuffle(all_periods)
        
        for day, period in all_periods:
            if period == 5: continue
            
            req_slots = [period]
            if duration == 2:
                if period not in (1, 3, 6, 7): continue
                if (day, period+1) not in PERIODS: continue
                if period == 4: continue
                req_slots = [period, period+1]
            
            # Check Conflicts
            slot_conflicts = []
            for p in req_slots:
                # Use your existing get_conflicting_entries function
                confs = get_conflicting_entries(day, p, fsc['faculty_id'], fsc['section_id'], fsc['class_id'])
                slot_conflicts.extend(confs)
            
            # FIX: Count Unique FSC IDs (index 0), not Reasons
            # The conflict list is [(fsc_id, reason), ...] based on your previous logs
            unique_ids = {c[0] for c in slot_conflicts}
            
            # RELAXED PRUNING:
            # Dynamic limits based on course type and depth
            base_limit = 8 if fsc['is_lab'] else 5
            depth_bonus = depth // 3  # Allow more conflicts at deeper levels
            limit = base_limit + depth_bonus
            if len(unique_ids) > limit:
                continue
            
            candidates.append({
                'day': day, 
                'req_slots': req_slots, 
                'conflicts': slot_conflicts, 
                'unique_ids': unique_ids
            })
        
        # Sort Candidates: Try LOWEST conflict count first (The "Min-Conflicts" Heuristic)
        candidates.sort(key=lambda x: len(x['unique_ids']))
        
        for cand in candidates:
            day = cand['day']
            req_slots = cand['req_slots']
            conflicts = cand['conflicts']
            
            sp_name = f"dfs_{depth}_{random.randint(100000,999999)}"
            try:
                cursor.execute(f"SAVEPOINT {sp_name}")
                
                # A. Remove Conflicts
                displaced_fscs = []
                processed_cf_ids = set()
                print(conflicts)
                for cf_item in conflicts:
                    cf_fsc_id = cf_item[0] # Index 0 is ID
                    
                    if cf_fsc_id in processed_cf_ids: continue
                    
                    cf_info = fetch_data.get_faculty_section_course(cursor, faculty_section_course_id=cf_fsc_id)
                    cf_slots = fetch_data.get_timetables(cursor, faculty_section_course_id=cf_fsc_id)
                    
                    if not cf_slots: continue
                    
                    for s in cf_slots:
                        delete_timetable_safe(cf_fsc_id, s['day'], s['period_id'])
                    
                    lost_hrs = len(cf_slots)
                    displaced_fscs.append({'fsc': cf_info, 'hrs_needed': lost_hrs})
                    processed_cf_ids.add(cf_fsc_id)

                # B. Insert Current Course
                for p in req_slots:
                    add_timetable_safe(fsc['id'], day, p)
                
                # C. Prepare Recursive State
                rem_current = hrs_needed - duration
                
                # Mix displaced with remaining. 
                next_pending = pending_courses[1:] + displaced_fscs
                if rem_current > 0:
                    next_pending.append({'fsc': fsc, 'hrs_needed': rem_current})
                
                if depth < 30:  # Increased depth limit for complex cases
                    if solve_recursively(next_pending, depth + 1):
                        cursor.execute(f"RELEASE SAVEPOINT {sp_name}")
                        return True
                
                raise Exception("Backtrack")

            except Exception as e:
                print(e.args)
                cursor.execute(f"ROLLBACK TO SAVEPOINT {sp_name}")
                continue
        
        return False

    # ==========================================
    # 4. EXECUTE GLOBAL FIXER
    # ==========================================
    print("\n=== Running Global Constraint Solver for Failed Allocations ===")
    
    # 1. Collect all courses that still have hrs > 0
    # failed_courses = []
    
    # # Check Labs
    # cursor.execute("SELECT * FROM `faculty_section_course` WHERE `hrs` > 0")
    # remaining_rows = cursor.fetchall()
    
    # for r in remaining_rows:
    #     # We need to manually calculate ACTUAL remaining based on DB because 
    #     # local variables in previous loops might not have synced perfectly if logical errors existed.
    #     # But 'hrs' column in DB is not updated by us? 
    #     # WAIT: Your previous code updates dictionary objects, not DB 'hrs' column.
    #     # We must rely on the counts in 'timetables' vs 'faculty_section_course'.
        
    #     cursor.execute("SELECT COUNT(*) as cnt FROM timetables WHERE faculty_section_course_id=%s", (r['id'],))
    #     allocated_hrs = cursor.fetchone()['cnt']
        
    #     # Total hrs required is in 'fsc.csv'? No, it's in 'faculty_section_course' table 'hrs' column?
    #     # Assuming 'hrs' in DB is the TARGET hours.
    #     target_hrs = r['hrs'] # This column usually means Total Hours per week
        
    #     needed = target_hrs - allocated_hrs
    #     if needed > 0:
    #         failed_courses.append({'fsc': r, 'hrs_needed': needed})

    # if not failed_courses:
    #     print("Success! No failed courses found.")
    # else:
    #     print(f"Found {len(failed_courses)} courses with pending hours. Attempting to solve...")
        
    #     # Multi-stage recovery process
    #     recovery_stages = [
    #         ("Stage 1: Simple backtracking", lambda: solve_recursively(failed_courses.copy())),
    #         ("Stage 2: Relaxed constraints", lambda: solve_with_relaxed_constraints(failed_courses.copy())),
    #         ("Stage 3: Aggressive reshuffling", lambda: solve_with_aggressive_reshuffling(failed_courses.copy()))
    #     ]
        
    #     for stage_name, stage_func in recovery_stages:
    #         print(f"\n=== {stage_name} ===")
    #         try:
    #             if stage_func():
    #                 print(f"{stage_name} Success! All courses allocated.")
    #                 db_connector.commit()
    #                 break
    #             else:
    #                 print(f"{stage_name} failed. Trying next approach...")
    #                 db_connector.rollback()
    #         except Exception as e:
    #             print(f"{stage_name} failed with error: {e}")
    #             db_connector.rollback()
    #     else:
    #         print("All recovery stages failed. The schedule may be unsatisfiable with current constraints.")
    #         # Optional: Keep partial solution or revert?
    #         # db_connector.rollback()
