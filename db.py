import sqlite3

conn = sqlite3.connect("lab4\\EECE435L-lab4-awh15-mmb78\\lab_db.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

cursor.execute("CREATE TABLE if not exists students (student_id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
cursor.execute("CREATE TABLE if not exists instructors (instructor_id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
cursor.execute("CREATE TABLE if not exists courses (course_id TEXT PRIMARY KEY, course_name TEXT, instructor_id TEXT, FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id))")

cursor.execute("CREATE TABLE if not exists student_courses (student_id TEXT, course_id TEXT, FOREIGN KEY(student_id) REFERENCES students(student_id), FOREIGN KEY(course_id) REFERENCES courses(course_id))")

conn.commit()
conn.close()