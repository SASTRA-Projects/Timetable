CREATE DATABASE IF NOT EXISTS university;
USE university;

-- 1. Basic Hierarchy
CREATE TABLE campus (
    campus_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE school (
    school_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    campus_id INT NOT NULL,
    FOREIGN KEY (campus_id) REFERENCES campus(campus_id)
);

CREATE TABLE building (
    building_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    campus_id INT NOT NULL,
    FOREIGN KEY (campus_id) REFERENCES campus(campus_id)
);

CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,        -- EDITED: Removed dept_code
    school_id INT NOT NULL,
    FOREIGN KEY (school_id) REFERENCES school(school_id)
);

-- 2. Academic Program Hierarchy
CREATE TABLE degree (
    degree_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL         -- EDITED: Removed degree_code
);

CREATE TABLE stream (
    stream_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL         -- EDITED: Removed stream_code
);

CREATE TABLE programme (
    programme_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,               -- EDITED: Removed programme_code
    dept_id INT NOT NULL,
    degree_id INT NOT NULL,
    stream_id INT NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    FOREIGN KEY (degree_id) REFERENCES degree(degree_id),
    FOREIGN KEY (stream_id) REFERENCES stream(stream_id)
);

-- 3. Courses and Offerings
CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL         -- EDITED: Removed course_code, course_type, etc.
);

CREATE TABLE programme_course (
    programme_id INT NOT NULL,
    course_id INT NOT NULL,
    semester INT NOT NULL,
    PRIMARY KEY (programme_id, course_id),
    FOREIGN KEY (programme_id) REFERENCES programme(programme_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- 4. Batches, Sections, Faculty
CREATE TABLE batch (
    batch_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    programme_id INT NOT NULL,
    FOREIGN KEY (programme_id) REFERENCES programme(programme_id)
);

CREATE TABLE section (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    batch_id INT NOT NULL,
    FOREIGN KEY (batch_id) REFERENCES batch(batch_id)
);

CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept_id INT NOT NULL,                     -- EDITED: Removed unnecessary school/campus data
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

-- 5. Faculty Course and Section Assignment
CREATE TABLE faculty_course (
    faculty_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (faculty_id, course_id),      -- EDITED: Removed campus_id, school_id from here
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE section_course (
    section_id INT NOT NULL,
    course_id INT NOT NULL,
    faculty_id INT NOT NULL,                  -- EDITED: Simplified, removed redundant info
    PRIMARY KEY (section_id, course_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

-- 6. Student Info
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    section_id INT NOT NULL,
    FOREIGN KEY (section_id) REFERENCES section(section_id)
);

-- 7. Room and Timetable
CREATE TABLE room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_no VARCHAR(10) NOT NULL,
    capacity INT NOT NULL,
    building_id INT NOT NULL,
    FOREIGN KEY (building_id) REFERENCES building(building_id)
);

CREATE TABLE timetable (
    timetable_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    course_id INT NOT NULL,
    faculty_id INT NOT NULL,
    room_id INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);
