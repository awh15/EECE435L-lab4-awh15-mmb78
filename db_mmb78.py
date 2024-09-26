import sqlite3
from lab2_mmb78 import Student, Instructor, Course

# Function to connect to the SQLite database
def connect():
    return sqlite3.connect('school_management.db')

# Function to create the required tables
def create_tables():
    conn = connect()
    c = conn.cursor()

    # Create Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')

    # Create Instructors table
    c.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')

    # Create Courses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT,
            instructor_id TEXT,
            FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id)
        )
    ''')

    # Create Enrollments table to track students enrolled in courses
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id TEXT,
            course_id TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    ''')

    conn.commit()
    conn.close()

# CRUD Functions for Students
def add_student(student):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (student.student_id, student.name, student.age, student.get_email()))
    conn.commit()
    conn.close()

def get_all_students():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    rows = c.fetchall()
    conn.close()

    students = []
    for row in rows:
        student = Student(name=row[1], age=row[2], email=row[3], student_id=row[0])
        students.append(student)
    return students

def update_student(student):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        UPDATE students SET name = ?, age = ?, email = ? WHERE student_id = ?
    ''', (student.name, student.age, student.get_email(), student.student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

# CRUD Functions for Instructors
def add_instructor(instructor):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
    conn.commit()
    conn.close()

def get_all_instructors():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM instructors')
    rows = c.fetchall()
    conn.close()

    instructors = []
    for row in rows:
        instructor = Instructor(name=row[1], age=row[2], email=row[3], instructor_id=row[0])
        instructors.append(instructor)
    return instructors

def update_instructor(instructor):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?
    ''', (instructor.name, instructor.age, instructor.get_email(), instructor.instructor_id))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
    conn.commit()
    conn.close()

# CRUD Functions for Courses
def add_course(course):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)
    ''', (course.course_id, course.course_name, course.instructor.instructor_id))
    conn.commit()
    conn.close()

def get_all_courses():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    rows = c.fetchall()
    conn.close()

    courses = []
    for row in rows:
        instructor = get_instructor_by_id(row[2])  # Assuming instructor retrieval by ID
        course = Course(course_id=row[0], course_name=row[1], instructor=instructor)
        courses.append(course)
    return courses

def update_course(course):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        UPDATE courses SET course_name = ?, instructor_id = ? WHERE course_id = ?
    ''', (course.course_name, course.instructor.instructor_id, course.course_id))
    conn.commit()
    conn.close()

def delete_course(course_id):
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
    conn.commit()
    conn.close()

# Helper function to get an instructor by ID
def get_instructor_by_id(instructor_id):
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM instructors WHERE instructor_id = ?', (instructor_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return Instructor(name=row[1], age=row[2], email=row[3], instructor_id=row[0])
    return None

def get_instructor_by_name(name):
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM instructors WHERE name = ?', (name,))
    row = c.fetchone()
    conn.close()

    if row:
        return Instructor(instructor_id=row[0], name=row[1], age=row[2], email=row[3])
    else:
        return None

# Enrollment Functions
def enroll_student(student_id, course_id):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)
    ''', (student_id, course_id))
    conn.commit()
    conn.close()

def get_enrollments_for_course(course_id):
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT student_id FROM enrollments WHERE course_id = ?', (course_id,))
    rows = c.fetchall()
    conn.close()

    students = []
    for row in rows:
        student = get_student_by_id(row[0])  # Assuming student retrieval by ID
        students.append(student)
    return students

def get_student_by_id(student_id):
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return Student(name=row[1], age=row[2], email=row[3], student_id=row[0])
    return None

    
def get_course_by_id(course_id):
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ?', (course_id,))
    row = c.fetchone()
    conn.close()

    if row:
        # Fetch instructor information for the course
        instructor = get_instructor_by_id(row[2])  # Assuming row[2] contains instructor_id
        # Fetch enrolled students for the course
        enrolled_students = get_enrollments_for_course(course_id)
        return Course(course_id=row[0], course_name=row[1], instructor=instructor, enrolled_students=enrolled_students)
    return None

def get_course_by_name(course_name):
    """Fetches a course by its name from the database."""
    conn = connect()
    c = conn.cursor()

    # Query the database for the course with the given course_name
    c.execute('SELECT * FROM courses WHERE course_name = ?', (course_name,))
    row = c.fetchone()
    conn.close()

    if row:
        # Assuming row[0] is course_id, row[1] is course_name, and row[2] is instructor_id
        instructor = get_instructor_by_id(row[2])  # Fetch the instructor by ID
        return Course(course_id=row[0], course_name=row[1], instructor=instructor)
    
    return None  # Return None if the course is not found

