import json
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox,
    QFormLayout, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox,
    QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
)

import sys
import csv

class Person:
    """
    Represents a person with a name, age, and email address.

    :param name: The name of the person.
    :param age: The age of the person.
    :param email: The email address of the person.
    """

    def __init__(self, name: str, age: int, email: str):
        """
        Initializes a new Person instance.

        :param name: The name of the person.
        :param age: The age of the person (must be non-negative).
        :param email: The email address of the person (must be valid).
        """
        self.name = name
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)

    def introduce(self):
        """
        Introduces the person by printing their name and age.
        """
        print(f"Hello, my name is {self.name}. I am {self.age} years old.")

    @staticmethod
    def validate_email(email: str):
        """
        Validates the format of an email address.

        :param email: The email address to validate.
        :raises ValueError: If the email format is invalid.
        :return: The validated email address.
        """
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return email
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_age(age: int):
        """
        Validates the age of a person.

        :param age: The age to validate.
        :raises ValueError: If the age is negative.
        :return: The validated age.
        """
        if age < 0:
            raise ValueError("Age cannot be negative")
        return age

    def to_dict(self):
        """
        Converts the Person instance to a dictionary.

        :return: A dictionary representation of the person.
        """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Person instance from a dictionary.

        :param data: A dictionary containing the person's data.
        :return: A new Person instance.
        """
        return cls(data['name'], data['age'], data['email'])


class Student(Person):
    """
    Represents a student, inheriting from the Person class.

    :param name: The name of the student.
    :param age: The age of the student.
    :param email: The email address of the student.
    :param student_id: The unique identifier for the student.
    """

    def __init__(self, name: str, age: int, email: str, student_id: str):
        """
        Initializes a new Student instance.

        :param name: The name of the student.
        :param age: The age of the student (must be non-negative).
        :param email: The email address of the student (must be valid).
        :param student_id: The unique identifier for the student.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Registers a course for the student.

        :param course: The course to register.
        """
        self.registered_courses.append(course)
        course.add_student(self)
        print(f"Course {course.course_name} has been registered for student {self.name}.")

    def to_dict(self):
        """
        Converts the Student instance to a dictionary.

        :return: A dictionary representation of the student.
        """
        return {
            **super().to_dict(),
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Student instance from a dictionary.

        :param data: A dictionary containing the student's data.
        :return: A new Student instance.
        """
        student = cls(data['name'], data['age'], data['email'], data['student_id'])
        return student


class Instructor(Person):
    """
    Represents an instructor, inheriting from the Person class.

    :param name: The name of the instructor.
    :param age: The age of the instructor.
    :param email: The email address of the instructor.
    :param instructor_id: The unique identifier for the instructor.
    """

    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        """
        Initializes a new Instructor instance.

        :param name: The name of the instructor.
        :param age: The age of the instructor (must be non-negative).
        :param email: The email address of the instructor (must be valid).
        :param instructor_id: The unique identifier for the instructor.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        :param course: The course to assign.
        """
        self.assigned_courses.append(course)
        course.instructor = self
        print(f"Instructor {self.name} has been assigned to course {course.course_name}.")

    def to_dict(self):
        """
        Converts the Instructor instance to a dictionary.

        :return: A dictionary representation of the instructor.
        """
        return {
            **super().to_dict(),
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an Instructor instance from a dictionary.

        :param data: A dictionary containing the instructor's data.
        :return: A new Instructor instance.
        """
        instructor = cls(data['name'], data['age'], data['email'], data['instructor_id'])
        return instructor


class Course:
    """
    Represents a course in the school management system.

    :param course_id: The unique identifier for the course.
    :param course_name: The name of the course.
    """

    def __init__(self, course_id: str, course_name: str):
        """
        Initializes a new Course instance.

        :param course_id: The unique identifier for the course.
        :param course_name: The name of the course.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

    def add_student(self, student):
        """
        Adds a student to the course.

        :param student: The student to add to the course.
        """
        self.enrolled_students.append(student)
        print(f"Student {student.name} has been added to course {self.course_name}.")

    def to_dict(self):
        """
        Converts the Course instance to a dictionary.

        :return: A dictionary representation of the course.
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Course instance from a dictionary.

        :param data: A dictionary containing the course's data.
        :return: A new Course instance.
        """
        course = cls(data['course_id'], data['course_name'])
        return course

    
students = []
instructors = []
courses = []


def save_data():
    """
    Save the current state of students, instructors, and courses to a JSON file.

    The function gathers data from the global lists of students, instructors, and courses,
    formats it into a dictionary structure, and writes it to a JSON file. The file path
    is set to a specific location on the user's machine.

    Raises:
        IOError: If there is an issue opening or writing to the file.
    """
    data = {
        "students": [{"name": s.name, "age": s.age, "email": s._email, "student_id": s.student_id} for s in students],
        "instructors": [{"name": i.name, "age": i.age, "email": i._email, "instructor_id": i.instructor_id, "assigned_courses": [c.course_id for c in i.assigned_courses]} for i in instructors],
        "courses": [{"course_id": c.course_id, "course_name": c.course_name, "enrolled_students": [s.student_id for s in c.enrolled_students], "instructor": c.instructor.instructor_id if c.instructor else None} for c in courses]
    }
    file_path = "C:\\Users\\Lenovo\\OneDrive - American University of Beirut\\EECE 435L\\lab2\\data.json"
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(data, file)
        msg = QMessageBox()
        msg.setWindowTitle("Save")
        msg.setText("Save successful.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()


def load_data():
    """
    Load student, instructor, and course data from a JSON file.

    This function reads data from a specified JSON file, clears the existing lists of
    students, instructors, and courses, and populates them with the loaded data. The
    function creates instances of `Student`, `Instructor`, and `Course` based on the
    data structure defined in the JSON file. It also establishes relationships between
    instructors and courses, as well as between students and courses.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contents cannot be parsed as JSON.
    """
    file_path = "C:\\Users\\Lenovo\\OneDrive - American University of Beirut\\EECE 435L\\lab2\\data.json"
    if file_path:
        with open(file_path, 'r') as file:
            data = json.load(file)

        students.clear()
        instructors.clear()
        courses.clear()

        for s_data in data["students"]:
            student = Student(s_data["name"], s_data["age"], s_data["email"], s_data["student_id"])
            students.append(student)

        for i_data in data["instructors"]:
            instructor = Instructor(i_data["name"], i_data["age"], i_data["email"], i_data["instructor_id"])
            for course_id in i_data["assigned_courses"]:
                course = next((c for c in courses if c.course_id == course_id), None)
                if course:
                    instructor.assign_course(course)
            instructors.append(instructor)

        for c_data in data["courses"]:
            course = Course(c_data["course_id"], c_data["course_name"])
            for student_id in c_data["enrolled_students"]:
                student = next((s for s in students if s.student_id == student_id), None)
                if student:
                    course.add_student(student)
            courses.append(course)
            if c_data["instructor"]:
                instructor = next((i for i in instructors if i.instructor_id == c_data["instructor"]), None)
                if instructor:
                    course.instructor = instructor
                    instructor.assign_course(course)



class StudentForm(QDialog):
    """
    Dialog for adding a new student.

    This dialog allows the user to input student information such as name, age,
    email, and student ID. Once the information is submitted, a new Student
    instance is created and added to the students list.

    Attributes:
        name_input (QLineEdit): Input field for the student's name.
        age_input (QLineEdit): Input field for the student's age.
        email_input (QLineEdit): Input field for the student's email.
        student_id_input (QLineEdit): Input field for the student's ID.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the dialog."""
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.email_input = QLineEdit()
        self.student_id_input = QLineEdit()

        layout.addRow(QLabel("Name:"), self.name_input)
        layout.addRow(QLabel("Age:"), self.age_input)
        layout.addRow(QLabel("Email:"), self.email_input)
        layout.addRow(QLabel("Student ID:"), self.student_id_input)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)

        layout.addRow(add_button)

        self.setLayout(layout)

    def add_student(self):
        """Creates a new Student instance and adds it to the students list."""
        name = self.name_input.text()
        age = int(self.age_input.text())
        email = self.email_input.text()
        student_id = self.student_id_input.text()
        s = Student(name, age, email, student_id)
        students.append(s)
        print(f"Student added: {name}, {age}, {email}, {student_id}")
        self.close()


class InstructorForm(QDialog):
    """
    Dialog for adding a new instructor.

    This dialog allows the user to input instructor information such as name, age,
    email, and instructor ID. Once the information is submitted, a new Instructor
    instance is created and added to the instructors list.

    Attributes:
        name_input (QLineEdit): Input field for the instructor's name.
        age_input (QLineEdit): Input field for the instructor's age.
        email_input (QLineEdit): Input field for the instructor's email.
        instructor_id_input (QLineEdit): Input field for the instructor's ID.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Instructor")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the dialog."""
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.email_input = QLineEdit()
        self.instructor_id_input = QLineEdit()

        layout.addRow(QLabel("Name:"), self.name_input)
        layout.addRow(QLabel("Age:"), self.age_input)
        layout.addRow(QLabel("Email:"), self.email_input)
        layout.addRow(QLabel("Instructor ID:"), self.instructor_id_input)

        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)

        layout.addRow(add_button)

        self.setLayout(layout)

    def add_instructor(self):
        """Creates a new Instructor instance and adds it to the instructors list."""
        name = self.name_input.text()
        age = int(self.age_input.text())
        email = self.email_input.text()
        instructor_id = self.instructor_id_input.text()
        i = Instructor(name, age, email, instructor_id)
        instructors.append(i)
        print(f"Instructor added: {name}, {age}, {email}, {instructor_id}")
        self.close()


class CourseForm(QDialog):
    """
    Dialog for adding a new course.

    This dialog allows the user to input course information such as course ID and
    course name. Once the information is submitted, a new Course instance is created
    and added to the courses list.

    Attributes:
        course_id_input (QLineEdit): Input field for the course ID.
        course_name_input (QLineEdit): Input field for the course name.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Course")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the dialog."""
        layout = QFormLayout()

        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()

        layout.addRow(QLabel("Course ID:"), self.course_id_input)
        layout.addRow(QLabel("Course Name:"), self.course_name_input)

        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)

        layout.addRow(add_button)

        self.setLayout(layout)

    def add_course(self):
        """Creates a new Course instance and adds it to the courses list."""
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        c = Course(course_id, course_name)
        courses.append(c)
        print(f"Course added: {course_id}, {course_name}")
        self.close()

        
class RegisterStudentsForm(QDialog):
    """
    Dialog for registering students in courses.

    This dialog allows the user to select a student and a course from
    dropdown menus. When the registration is confirmed, the selected student
    is registered in the selected course.

    Attributes:
        student_input (QComboBox): Dropdown for selecting a student.
        course_input (QComboBox): Dropdown for selecting a course.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Students")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the dialog."""
        layout = QFormLayout()

        self.student_input = QComboBox()
        self.course_input = QComboBox()
        for s in students:
            self.student_input.addItem(f"{s.student_id} - {s.name}")
        for c in courses:
            self.course_input.addItem(f"{c.course_id} - {c.course_name}")

        layout.addRow(QLabel("Student:"), self.student_input)
        layout.addRow(QLabel("Course:"), self.course_input)

        add_button = QPushButton("Register Student")
        add_button.clicked.connect(self.register_students)

        layout.addRow(add_button)

        self.setLayout(layout)
    
    def register_students(self):
        """Registers the selected student in the selected course."""
        student_id = self.student_input.currentText().split("-")[0].strip()
        course_id = self.course_input.currentText().split("-")[0].strip()
        s = next((s for s in students if s.student_id == student_id), None)
        c = next((c for c in courses if c.course_id == course_id), None)
        if s and c:
            s.register_course(c)
            print(f"Student {s.name} has been registered in course {c.course_name}.")
        else:
            print("Invalid student or course.")
        self.close()


class AssignInstructorsForm(QDialog):
    """
    Dialog for assigning instructors to courses.

    This dialog allows the user to select an instructor and a course from
    dropdown menus. When the assignment is confirmed, the selected instructor
    is assigned to the selected course.

    Attributes:
        instructor_input (QComboBox): Dropdown for selecting an instructor.
        course_input (QComboBox): Dropdown for selecting a course.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assign Instructors")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the dialog."""
        layout = QFormLayout()

        self.instructor_input = QComboBox()
        self.course_input = QComboBox()
        for i in instructors:
            self.instructor_input.addItem(f"{i.instructor_id} - {i.name}")
        for c in courses:
            self.course_input.addItem(f"{c.course_id} - {c.course_name}")

        layout.addRow(QLabel("Instructor:"), self.instructor_input)
        layout.addRow(QLabel("Course:"), self.course_input)

        add_button = QPushButton("Assign Instructor")
        add_button.clicked.connect(self.assign_instructor)

        layout.addRow(add_button)

        self.setLayout(layout)
    
    def assign_instructor(self):
        """Assigns the selected instructor to the selected course."""
        instructor_id = self.instructor_input.currentText().split("-")[0].strip()
        course_id = self.course_input.currentText().split("-")[0].strip()
        i = next((i for i in instructors if i.instructor_id == instructor_id), None)
        c = next((c for c in courses if c.course_id == course_id), None)
        if i and c:
            i.assign_course(c)
            print(f"Instructor {i.name} has been assigned to course {c.course_name}.")
        else:
            print("Invalid instructor or course.")
        self.close()

        
        
        
        

class EditRecordDialog(QDialog):
    """
    Dialog for editing records (students, instructors, or courses).

    This dialog allows the user to modify the attributes of a selected 
    record (student, instructor, or course) and save the changes.

    Attributes:
        fields (list): The fields of the record to be edited.
        record (Union[Student, Instructor, Course]): The record being edited.
        name (QLineEdit): Input field for the name.
        age (QLineEdit): Input field for the age (only for students and instructors).
        email (QLineEdit): Input field for the email (only for students and instructors).
        instructor (QComboBox): Dropdown for selecting an instructor (only for courses).
    """

    def __init__(self, record, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Record")
        self.fields = fields
        self.record = record
        
        layout = QFormLayout()
        
        if isinstance(record, Course):
            self.name = QLineEdit(record.course_name)
            layout.addRow(QLabel("Course name"), self.name)
            self.instructor = QComboBox()
            for i in instructors:
                self.instructor.addItem(f"{i.instructor_id} - {i.name}")
            layout.addRow(QLabel("Instructor:"), self.instructor)
        else:
            self.name = QLineEdit(record.name)
            self.age = QLineEdit(str(record.age))
            self.email = QLineEdit(record._email)
            layout.addRow(QLabel("Name"), self.name)
            layout.addRow(QLabel("Age"), self.age)
            layout.addRow(QLabel("Email"), self.email)

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.save_changes)
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def save_changes(self):
        """Saves the changes made to the record."""
        if isinstance(self.record, Course):
            instructor_id = self.instructor.currentText().split(" - ")[0]
            i = next((i for i in instructors if i.instructor_id == instructor_id), None)
            c = next((c for c in courses if c.course_id == self.record.course_id), None)
            c.instructor = i
            c.course_name = self.name.text()
        elif isinstance(self.record, Student):
            s = next((s for s in students if s.student_id == self.record.student_id), None)
            s.name = self.name.text()
            s.age = int(self.age.text())
            s._email = self.email.text()
        else:
            i = next((i for i in instructors if i.instructor_id == self.record.instructor_id), None)
            i.name = self.name.text()
            i.age = int(self.age.text())
            i._email = self.email.text()
        
        self.close()


class DisplayRecordsWindow(QMainWindow):
    """
    Main window for displaying records of students, instructors, and courses.

    This window contains tabs for each type of record, and allows users to 
    view, edit, and delete records.

    Attributes:
        tab_widget (QTabWidget): Widget for holding multiple tabs.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 600, 400)

        self.tab_widget = QTabWidget()

        self.tab_widget.addTab(self.create_table_tab("Students", students, ["student_id", "name", "age", "email"]), "Students")
        self.tab_widget.addTab(self.create_table_tab("Instructors", instructors, ["instructor_id", "name", "age", "email"]), "Instructors")
        self.tab_widget.addTab(self.create_table_tab("Courses", courses, ["course_id", "course_name", "instructor"]), "Courses")

        self.setCentralWidget(self.tab_widget)

    def create_table_tab(self, tab_name, records, fields):
        """
        Create a tab with a table for displaying records.

        Parameters:
            tab_name (str): The name of the tab (e.g., "Students").
            records (list): The list of records to display.
            fields (list): The fields of the records.

        Returns:
            QWidget: The created tab.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        search_bar = QLineEdit()
        search_bar.setPlaceholderText(f"Search {tab_name}")
        search_bar.textChanged.connect(lambda: self.filter_table(search_bar, table, records))

        table = QTableWidget()
        table.setRowCount(len(records))
        table.setColumnCount(len(fields) + 2)
        table.setHorizontalHeaderLabels(fields + ["Edit", "Delete"])

        self.populate_table(table, records, fields, tab_name)

        layout.addWidget(search_bar)
        layout.addWidget(table)
        tab.setLayout(layout)
        return tab

    def populate_table(self, table, records, fields, tab_name):
        """
        Fill the table with data and add Edit/Delete buttons.

        Parameters:
            table (QTableWidget): The table to populate.
            records (list): The list of records.
            fields (list): The fields to display.
            tab_name (str): The name of the tab (e.g., "Students").
        """
        table.setRowCount(len(records))
        for row, record in enumerate(records):
            if tab_name == "Courses":
                table.setItem(row, 0, QTableWidgetItem(record.course_id))
                table.setItem(row, 1, QTableWidgetItem(record.course_name))
                table.setItem(row, 2, QTableWidgetItem(record.instructor.name if record.instructor else "None"))
            elif tab_name == "Students":
                table.setItem(row, 0, QTableWidgetItem(record.student_id))
                table.setItem(row, 1, QTableWidgetItem(record.name))
                table.setItem(row, 2, QTableWidgetItem(str(record.age)))
                table.setItem(row, 3, QTableWidgetItem(record._email))
            else:
                table.setItem(row, 0, QTableWidgetItem(record.instructor_id))
                table.setItem(row, 1, QTableWidgetItem(record.name))
                table.setItem(row, 2, QTableWidgetItem(str(record.age)))
                table.setItem(row, 3, QTableWidgetItem(record._email))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, r=record, f=fields: self.edit_record(r, f, table))
            table.setCellWidget(row, len(fields), edit_button)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=row: self.delete_record(r, records, table, tab_name))
            table.setCellWidget(row, len(fields) + 1, delete_button)

    def filter_table(self, search_bar, table, records):
        """Filter the table based on search input."""
        search_text = search_bar.text().lower()
        for row, record in enumerate(records):
            try:
                if search_text in record.name.lower():
                    table.setRowHidden(row, False)
                else:
                    table.setRowHidden(row, True)
            except AttributeError:
                if search_text in record.course_name.lower():
                    table.setRowHidden(row, False)
                else:
                    table.setRowHidden(row, True)

    def edit_record(self, record, fields, table):
        """Open an edit dialog to modify the selected record."""
        dialog = EditRecordDialog(record, fields)
        if dialog.exec_():
            self.populate_table(table, students, fields)
        self.close()

    def delete_record(self, row, records, table, tab_name):
        """Delete a record and update the table."""
        records.pop(row)
        self.populate_table(table, records, [table.horizontalHeaderItem(i).text() for i in range(table.columnCount() - 2)], tab_name)

class MainWindow(QMainWindow):
    """
    Main application window for the School Management System.

    This window provides buttons for adding students, instructors, 
    courses, registering students, assigning instructors, displaying 
    records, exporting data to CSV, and saving data to a file.

    Attributes:
        central_widget (QWidget): The central widget of the main window.
    """

    def __init__(self):
        """
        Initialize the main window and its UI.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface components of the main window.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        student_button = QPushButton("Add Student")
        student_button.clicked.connect(self.open_student_form)
        layout.addWidget(student_button)

        instructor_button = QPushButton("Add Instructor")
        instructor_button.clicked.connect(self.open_instructor_form)
        layout.addWidget(instructor_button)

        course_button = QPushButton("Add Course")
        course_button.clicked.connect(self.open_course_form)
        layout.addWidget(course_button)
        
        register_button = QPushButton("Register Students")
        register_button.clicked.connect(self.register_students)
        layout.addWidget(register_button)
        
        assign_button = QPushButton("Assign Instructors")
        assign_button.clicked.connect(self.assign_instructors)
        layout.addWidget(assign_button)
        
        display_button = QPushButton("Display Records")
        display_button.clicked.connect(self.display_records)
        layout.addWidget(display_button)
        
        csv_button = QPushButton("Export CSV")
        csv_button.clicked.connect(self.export_csv)
        layout.addWidget(csv_button)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(save_data)
        layout.addWidget(save_button)

        central_widget.setLayout(layout)

    def open_student_form(self):
        """Open the dialog for adding a new student."""
        self.student_form = StudentForm()
        self.student_form.exec_()

    def open_instructor_form(self):
        """Open the dialog for adding a new instructor."""
        self.instructor_form = InstructorForm()
        self.instructor_form.exec_()

    def open_course_form(self):
        """Open the dialog for adding a new course."""
        self.course_form = CourseForm()
        self.course_form.exec_()
        
    def register_students(self):
        """Open the dialog for registering students to courses."""
        self.register_students_form = RegisterStudentsForm()
        self.register_students_form.exec_()
        
    def assign_instructors(self):
        """Open the dialog for assigning instructors to courses."""
        self.assign_instructors_form = AssignInstructorsForm()
        self.assign_instructors_form.exec_()
        
    def display_records(self):
        """Open the window for displaying student, instructor, and course records."""
        self.display_records_form = DisplayRecordsWindow()
        self.display_records_form.show()
        
    def export_csv(self):
        """Export student, instructor, and course data to a CSV file."""
        file_path = "school_data.csv"
        
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                
                writer.writerow(["Students"])
                writer.writerow(["Name", "Age", "Email", "Student ID"])
                for student in students:
                    writer.writerow([student.name, student.age, student._email, student.student_id])

                writer.writerow([])  # Blank line

                writer.writerow(["Instructors"])
                writer.writerow(["Name", "Age", "Email", "Instructor ID"])
                for instructor in instructors:
                    writer.writerow([instructor.name, instructor.age, instructor._email, instructor.instructor_id])

                writer.writerow([])  # Blank line

                writer.writerow(["Courses"])
                writer.writerow(["Course ID", "Course Name", "Instructor", "Enrolled Students"])
                for course in courses:
                    instructor_name = course.instructor.name if course.instructor else "None"
                    enrolled_students = ", ".join([student.name for student in course.enrolled_students])
                    writer.writerow([course.course_id, course.course_name, instructor_name, enrolled_students])

            QMessageBox.information(self, "Success", f"Data exported successfully to {file_path}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting: {e}")


if __name__ == "__main__":
    load_data()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
