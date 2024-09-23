import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox,
    QFormLayout, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox,
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget,
    QHBoxLayout, QDialogButtonBox, 
)
import sys
import csv
import sqlite3

def validate_email(email: str):
    """
    Validates an email address format.

    This function checks if the given email address follows a valid pattern.
    The pattern allows alphanumeric characters, dots, and hyphens in the 
    username and domain, and requires a top-level domain at the end.

    :param email: The email address to validate.
    :type email: str
    :return: A match object if the email is valid, None otherwise.
    :rtype: re.Match or None

    :raises re.error: If the regex pattern is invalid.
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

        

conn = sqlite3.connect("lab4\\EECE435L-lab4-awh15-mmb78\\lab_db.db")
cursor = conn.cursor()

class StudentForm(QDialog):
    """
    A dialog window for adding a student to the database.

    This class provides a form with fields for entering student details such as
    name, age, email, and student ID. It handles user input and adds the student
    to the SQLite database.

    :param QDialog: Inherits from QDialog to provide a modal dialog window.
    """

    def __init__(self):
        """
        Initializes the StudentForm dialog.

        This method sets the window title and calls `setup_ui()` to create the
        form layout and input fields.
        """
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the student form.

        This method creates a form layout and adds input fields for the student's
        name, age, email, and student ID. It also adds a button for submitting the
        form, which is connected to the `add_student()` method.
        """
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
        """
        Adds the student to the database.

        This method retrieves the values from the input fields, inserts the
        student details into the SQLite database, and commits the transaction.

        :raises ValueError: If the age input is not an integer.
        
        :return: None
        """
        name = self.name_input.text()
        age = int(self.age_input.text())
        email = self.email_input.text()
        student_id = self.student_id_input.text()
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (student_id, name, age, email))
        conn.commit()
        print(f"Student added: {name}, {age}, {email}, {student_id}")
        self.close()


class InstructorForm(QDialog):
    """
    A dialog window for adding an instructor to the database.

    This class provides a form with fields for entering instructor details such as
    name, age, email, and instructor ID. It handles user input and adds the instructor
    to the SQLite database.

    :param QDialog: Inherits from QDialog to provide a modal dialog window.
    """

    def __init__(self):
        """
        Initializes the InstructorForm dialog.

        This method sets the window title and calls `setup_ui()` to create the
        form layout and input fields.
        """
        super().__init__()
        self.setWindowTitle("Add Instructor")
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the instructor form.

        This method creates a form layout and adds input fields for the instructor's
        name, age, email, and instructor ID. It also adds a button for submitting the
        form, which is connected to the `add_instructor()` method.
        """
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
        """
        Adds the instructor to the database.

        This method retrieves the values from the input fields, inserts the
        instructor details into the SQLite database, and commits the transaction.

        :raises ValueError: If the age input is not an integer.
        
        :return: None
        """
        name = self.name_input.text()
        age = int(self.age_input.text())
        email = self.email_input.text()
        instructor_id = self.instructor_id_input.text()
        cursor.execute("INSERT INTO instructors VALUES (?, ?, ?, ?)", (instructor_id, name, age, email))
        conn.commit()
        print(f"Instructor added: {name}, {age}, {email}, {instructor_id}")
        self.close()


class CourseForm(QDialog):
    """
    A dialog window for adding a course to the database.

    This class provides a form with fields for entering course details such as
    course ID and course name. It handles user input and adds the course
    to the SQLite database.

    :param QDialog: Inherits from QDialog to provide a modal dialog window.
    """

    def __init__(self):
        """
        Initializes the CourseForm dialog.

        This method sets the window title and calls `setup_ui()` to create the
        form layout and input fields.
        """
        super().__init__()
        self.setWindowTitle("Add Course")
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the course form.

        This method creates a form layout and adds input fields for the course's
        ID and name. It also adds a button for submitting the form, which is
        connected to the `add_course()` method.
        """
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
        """
        Adds the course to the database.

        This method retrieves the values from the input fields, inserts the
        course details into the SQLite database, and commits the transaction.
        
        The course is added with a placeholder (`None`) for any additional course
        details that may be required later.

        :return: None
        """
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        cursor.execute("INSERT INTO courses VALUES (?, ?, ?)", (course_id, course_name, None))
        conn.commit()
        print(f"Course added: {course_id}, {course_name}")
        self.close()

        
class RegisterStudentsForm(QDialog):
    """
    A dialog window for registering students in courses.

    This class provides a form with dropdowns to select a student and a course.
    It retrieves available students and courses from the database, displays them 
    in `QComboBox` dropdowns, and registers the selected student for the chosen course.

    :param QDialog: Inherits from QDialog to provide a modal dialog window.
    """

    def __init__(self):
        """
        Initializes the RegisterStudentsForm dialog.

        This method sets the window title and calls `setup_ui()` to create the
        form layout and input fields. The student and course data are loaded
        from the database and added to the dropdowns.
        """
        super().__init__()
        self.setWindowTitle("Register Students")
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the student registration form.

        This method creates a form layout and adds dropdown fields for selecting
        a student and a course. The available students and courses are retrieved
        from the SQLite database and displayed in the `QComboBox` widgets. It also
        adds a button for submitting the form, which is connected to the 
        `register_students()` method.
        """
        layout = QFormLayout()

        self.student_input = QComboBox()
        self.course_input = QComboBox()

        # Populate student dropdown
        cursor.execute("SELECT * FROM students")
        for s in cursor.fetchall():
            self.student_input.addItem(f"{s[0]} - {s[1]}")

        # Populate course dropdown
        cursor.execute("SELECT * FROM courses")
        for c in cursor.fetchall():
            self.course_input.addItem(f"{c[0]} - {c[1]}")

        layout.addRow(QLabel("Student:"), self.student_input)
        layout.addRow(QLabel("Course:"), self.course_input)

        add_button = QPushButton("Register Student")
        add_button.clicked.connect(self.register_students)

        layout.addRow(add_button)

        self.setLayout(layout)
    
    def register_students(self):
        """
        Registers the selected student for the selected course.

        This method retrieves the selected student ID and course ID from the
        dropdowns. It checks if the student and course exist in the database,
        and if so, it registers the student in the course by inserting a record
        into the `student_courses` table.

        :raises LookupError: If the selected student or course is invalid.

        :return: None
        """
        student_id = self.student_input.currentText().split("-")[0].strip()
        course_id = self.course_input.currentText().split("-")[0].strip()

        # Verify student and course exist
        cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        s = cursor.fetchone()
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
        c = cursor.fetchone()

        if s and c:
            cursor.execute("INSERT INTO student_courses VALUES (?, ?)", (student_id, course_id))
            conn.commit()
            print(f"Student {s[1]} has been registered in course {c[1]}.")
        else:
            print("Invalid student or course.")
        
        self.close()

        

class AssignInstructorsForm(QDialog):
    """
    A dialog window for assigning instructors to courses.

    This class provides a form with dropdowns to select an instructor and a course.
    It retrieves available instructors and courses from the database, displays them 
    in `QComboBox` dropdowns, and assigns the selected instructor to the chosen course.

    :param QDialog: Inherits from QDialog to provide a modal dialog window.
    """

    def __init__(self):
        """
        Initializes the AssignInstructorsForm dialog.

        This method sets the window title and calls `setup_ui()` to create the
        form layout and input fields. The instructor and course data are loaded
        from the database and added to the dropdowns.
        """
        super().__init__()
        self.setWindowTitle("Assign Instructors")
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the instructor assignment form.

        This method creates a form layout and adds dropdown fields for selecting
        an instructor and a course. The available instructors and courses are retrieved
        from the SQLite database and displayed in the `QComboBox` widgets. It also
        adds a button for submitting the form, which is connected to the 
        `assign_instructor()` method.
        """
        layout = QFormLayout()

        self.instructor_input = QComboBox()
        self.course_input = QComboBox()

        # Populate instructor dropdown
        cursor.execute("SELECT * FROM instructors")
        for i in cursor.fetchall():
            self.instructor_input.addItem(f"{i[0]} - {i[1]}")

        # Populate course dropdown
        cursor.execute("SELECT * FROM courses")
        for c in cursor.fetchall():
            self.course_input.addItem(f"{c[0]} - {c[1]}")

        layout.addRow(QLabel("Instructor:"), self.instructor_input)
        layout.addRow(QLabel("Course:"), self.course_input)

        add_button = QPushButton("Assign Instructor")
        add_button.clicked.connect(self.assign_instructor)

        layout.addRow(add_button)

        self.setLayout(layout)

    def assign_instructor(self):
        """
        Assigns the selected instructor to the selected course.

        This method retrieves the selected instructor ID and course ID from the
        dropdowns. It checks if both the instructor and course exist in the
        database, and if so, it updates the course record to assign the instructor.

        :raises LookupError: If the selected instructor or course is invalid.

        :return: None
        """
        instructor_id = self.instructor_input.currentText().split("-")[0].strip()
        course_id = self.course_input.currentText().split("-")[0].strip()

        # Verify instructor and course exist
        cursor.execute("SELECT * FROM instructors WHERE instructor_id=?", (instructor_id,))
        i = cursor.fetchone()
        cursor.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
        c = cursor.fetchone()

        if i and c:
            cursor.execute("UPDATE courses SET instructor_id=? WHERE course_id=?", (instructor_id, course_id))
            print(f"Instructor {i[1]} has been assigned to course {c[1]}.")
        else:
            print("Invalid instructor or course.")
        
        self.close()

        
        

class DisplayRecordsWindow(QMainWindow):
    """
    A main window for displaying and managing records in the School Management System.

    This class provides a user interface for viewing and managing students, instructors,
    and courses. It includes tabs for each type of record, with search functionality and
    options to edit or delete entries.

    :param QMainWindow: Inherits from QMainWindow to provide a main application window.
    """

    def __init__(self):
        """
        Initializes the DisplayRecordsWindow.

        This method sets the window title and dimensions, creates tabs for students,
        instructors, and courses, and sets up the respective UI elements for each tab.
        """
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()

        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.instructor_tab, "Instructors")
        self.tabs.addTab(self.course_tab, "Courses")

        self.setup_student_tab()
        self.setup_instructor_tab()
        self.setup_course_tab()

    def setup_student_tab(self):
        """
        Sets up the user interface for the students tab.

        This method creates a layout with a search bar and a table to display student records.
        It populates the table with student data and connects the search functionality.
        """
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.student_search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_students)
        search_layout.addWidget(self.student_search_input)
        search_layout.addWidget(search_button)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)  
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email", "Actions"])

        layout.addLayout(search_layout)
        layout.addWidget(self.student_table)

        self.student_tab.setLayout(layout)
        self.load_students()

    def load_students(self):
        """
        Loads student records from the database and populates the student table.

        This method executes a query to fetch all student records, clears the current
        table contents, and inserts the new data along with action buttons for editing
        and deleting records.
        """
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        self.student_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.student_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, row=row_data: self.edit_student(row))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_data: self.delete_student(row))

            self.student_table.setCellWidget(row_idx, 4, self.create_action_buttons(edit_button, delete_button))

    def create_action_buttons(self, edit_button, delete_button):
        """
        Creates a container for action buttons (edit and delete).

        :param edit_button: QPushButton for editing a record.
        :param delete_button: QPushButton for deleting a record.
        :return: QWidget containing the action buttons.
        """
        action_layout = QHBoxLayout()
        action_layout.addWidget(edit_button)
        action_layout.addWidget(delete_button)
        container = QWidget()
        container.setLayout(action_layout)
        return container

    def search_students(self):
        """
        Searches for students based on the input in the search field.

        This method retrieves students whose names or IDs match the search input and
        updates the student table to display the results.
        """
        search_value = self.student_search_input.text()

        query = "SELECT * FROM students WHERE name LIKE ? OR student_id = ?"
        cursor.execute(query, ('%' + search_value + '%', search_value))
        rows = cursor.fetchall()

        self.student_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.student_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, row=row_data: self.edit_student(row))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_data: self.delete_student(row))

            self.student_table.setCellWidget(row_idx, 4, self.create_action_buttons(edit_button, delete_button))

    def edit_student(self, row):
        """
        Opens a dialog to edit the selected student record.

        :param row: The row data of the student to edit.
        """
        dialog = EditStudentDialog(row)
        if dialog.exec_() == QDialog.Accepted:
            self.load_students()

    def delete_student(self, row):
        """
        Deletes the selected student record after user confirmation.

        :param row: The row data of the student to delete.
        """
        confirm = QMessageBox.question(self, "Delete Student", f"Are you sure you want to delete {row[1]}?", 
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            cursor.execute("DELETE FROM students WHERE id=?", (row[0],))
            conn.commit()
            self.load_students()

    def setup_instructor_tab(self):
        """
        Sets up the user interface for the instructors tab.

        This method creates a layout with a search bar and a table to display instructor records.
        It populates the table with instructor data and connects the search functionality.
        """
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.instructor_search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_instructors)
        search_layout.addWidget(self.instructor_search_input)
        search_layout.addWidget(search_button)

        self.instructor_table = QTableWidget()
        self.instructor_table.setColumnCount(5)
        self.instructor_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email", "Actions"])

        layout.addLayout(search_layout)
        layout.addWidget(self.instructor_table)

        self.instructor_tab.setLayout(layout)
        self.load_instructors()

    def load_instructors(self):
        """
        Loads instructor records from the database and populates the instructor table.

        This method executes a query to fetch all instructor records, clears the current
        table contents, and inserts the new data along with action buttons for editing
        and deleting records.
        """
        cursor.execute("SELECT * FROM instructors")
        rows = cursor.fetchall()

        self.instructor_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.instructor_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, row=row_data: self.edit_instructor(row))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_data: self.delete_instructor(row))

            self.instructor_table.setCellWidget(row_idx, 4, self.create_action_buttons(edit_button, delete_button))

    def search_instructors(self):
        """
        Searches for instructors based on the input in the search field.

        This method retrieves instructors whose names or IDs match the search input and
        updates the instructor table to display the results.
        """
        search_value = self.instructor_search_input.text()

        query = "SELECT * FROM instructors WHERE name LIKE ? OR instructor_id = ?"
        cursor.execute(query, ('%' + search_value + '%', search_value))
        rows = cursor.fetchall()

        self.instructor_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.instructor_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, row=row_data: self.edit_instructor(row))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_data: self.delete_instructor(row))

            self.instructor_table.setCellWidget(row_idx, 4, self.create_action_buttons(edit_button, delete_button))

    def edit_instructor(self, row):
        """
        Opens a dialog to edit the selected instructor record.

        :param row: The row data of the instructor to edit.
        """
        dialog = EditInstructorDialog(row)
        if dialog.exec_() == QDialog.Accepted:
            self.load_instructors()

    def delete_instructor(self, row):
        """
        Deletes the selected instructor record after user confirmation.

        :param row: The row data of the instructor to delete.
        """
        confirm = QMessageBox.question(self, "Delete Instructor", f"Are you sure you want to delete {row[1]}?", 
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            cursor.execute("DELETE FROM instructors WHERE id=?", (row[0],))
            conn.commit()
            self.load_instructors()

    def setup_course_tab(self):
        """
        Sets up the user interface for the courses tab.

        This method creates a layout with a search bar and a table to display course records.
        It populates the table with course data and connects the search functionality.
        """
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.course_search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_courses)
        search_layout.addWidget(self.course_search_input)
        search_layout.addWidget(search_button)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(["ID", "Name", "Instructor"])

        layout.addLayout(search_layout)
        layout.addWidget(self.course_table)

        self.course_tab.setLayout(layout)
        self.load_courses()

    def load_courses(self):
        """
        Loads course records from the database and populates the course table.

        This method executes a query to fetch all course records, clears the current
        table contents, and inserts the new data.
        """
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()

        self.course_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.course_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def search_courses(self):
        """
        Searches for courses based on the input in the search field.

        This method retrieves courses whose names or IDs match the search input and
        updates the course table to display the results.
        """
        search_value = self.course_search_input.text()

        query = "SELECT * FROM courses WHERE course_name LIKE ? OR course_id = ?"
        cursor.execute(query, ('%' + search_value + '%', search_value))
        rows = cursor.fetchall()

        self.course_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.course_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))



class EditStudentDialog(QDialog):
    """
    A dialog for editing student records.

    This class provides a user interface for editing student information, allowing
    the user to change the name and age of a selected student.

    :param QDialog: Inherits from QDialog to provide a modal dialog interface.
    :param student_data: A tuple containing the current data of the student to be edited.
    """

    def __init__(self, student_data):
        """
        Initializes the EditStudentDialog.

        :param student_data: A tuple containing the current data of the student to be edited.
        """
        super().__init__()

        self.student_data = student_data

        self.setWindowTitle("Edit Student")
        layout = QFormLayout()

        self.id_field = QLabel(str(student_data[0]))
        self.name_field = QLineEdit(student_data[1])
        self.age_field = QLineEdit(str(student_data[2]))

        layout.addRow("ID", self.id_field)
        layout.addRow("Name", self.name_field)
        layout.addRow("Age", self.age_field)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        """
        Updates the student record in the database with the new values from the input fields.

        This method is called when the user clicks the OK button. It executes an UPDATE
        query to change the name and age of the student in the database based on the
        provided student ID.
        """
        cursor.execute("UPDATE students SET name=?, age=? WHERE student_id=?", 
                       (self.name_field.text(), self.age_field.text(), self.student_data[0]))
        conn.commit()
        super().accept()


class EditInstructorDialog(QDialog):
    """
    A dialog for editing instructor records.

    This class provides a user interface for editing instructor information, allowing
    the user to change the name and subject of a selected instructor.

    :param QDialog: Inherits from QDialog to provide a modal dialog interface.
    :param instructor_data: A tuple containing the current data of the instructor to be edited.
    """

    def __init__(self, instructor_data):
        """
        Initializes the EditInstructorDialog.

        :param instructor_data: A tuple containing the current data of the instructor to be edited.
        """
        super().__init__()

        self.instructor_data = instructor_data

        self.setWindowTitle("Edit Instructor")
        layout = QFormLayout()

        self.id_field = QLabel(str(instructor_data[0]))
        self.name_field = QLineEdit(instructor_data[1])
        self.subject_field = QLineEdit(instructor_data[2])

        layout.addRow("ID", self.id_field)
        layout.addRow("Name", self.name_field)
        layout.addRow("Subject", self.subject_field)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        """
        Updates the instructor record in the database with the new values from the input fields.

        This method is called when the user clicks the OK button. It executes an UPDATE
        query to change the name and subject of the instructor in the database based on the
        provided instructor ID.
        """
        cursor.execute("UPDATE instructors SET name=?, subject=? WHERE instructor_id=?", 
                       (self.name_field.text(), self.subject_field.text(), self.instructor_data[0]))
        conn.commit()
        super().accept()
   
        
        
        
        
        
        

class MainWindow(QMainWindow):
    """
    Main application window for the School Management System.

    This class provides the main interface for the application, allowing users to
    perform various actions related to students, instructors, and courses.

    :param QMainWindow: Inherits from QMainWindow to provide the main window functionality.
    """

    def __init__(self):
        """
        Initializes the MainWindow and sets up the UI.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface components of the main window.

        This method sets up buttons for adding students, instructors, and courses,
        registering students, assigning instructors, displaying records, and exporting data to CSV.
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

        central_widget.setLayout(layout)

    def open_student_form(self):
        """
        Opens the dialog for adding a new student.

        This method creates an instance of the StudentForm and displays it as a modal dialog.
        """
        self.student_form = StudentForm()
        self.student_form.exec_()

    def open_instructor_form(self):
        """
        Opens the dialog for adding a new instructor.

        This method creates an instance of the InstructorForm and displays it as a modal dialog.
        """
        self.instructor_form = InstructorForm()
        self.instructor_form.exec_()

    def open_course_form(self):
        """
        Opens the dialog for adding a new course.

        This method creates an instance of the CourseForm and displays it as a modal dialog.
        """
        self.course_form = CourseForm()
        self.course_form.exec_()

    def register_students(self):
        """
        Opens the dialog for registering students to courses.

        This method creates an instance of the RegisterStudentsForm and displays it as a modal dialog.
        """
        self.register_students_form = RegisterStudentsForm()
        self.register_students_form.exec_()

    def assign_instructors(self):
        """
        Opens the dialog for assigning instructors to courses.

        This method creates an instance of the AssignInstructorsForm and displays it as a modal dialog.
        """
        self.assign_instructors_form = AssignInstructorsForm()
        self.assign_instructors_form.exec_()

    def display_records(self):
        """
        Opens the window for displaying student, instructor, and course records.

        This method creates an instance of the DisplayRecordsWindow and shows it.
        """
        self.display_records_form = DisplayRecordsWindow()
        self.display_records_form.show()

    def export_csv(self):
        """
        Exports the current records of students, instructors, and courses to a CSV file.

        This method generates a CSV file named "school_data.csv" containing the details of
        students, instructors, and courses, including enrolled students for each course.
        """
        file_path = "lab2/school_data.csv"

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(["Students"])
                writer.writerow(["Name", "Age", "Email", "Student ID"])
                cursor.execute("SELECT * FROM students")
                for student in cursor.fetchall():
                    writer.writerow([student[1], student[2], student[3], student[0]])

                writer.writerow([])

                writer.writerow(["Instructors"])
                writer.writerow(["Name", "Age", "Email", "Instructor ID"])
                cursor.execute("SELECT * FROM instructors")
                for instructor in cursor.fetchall():
                    writer.writerow([instructor[1], instructor[2], instructor[3], instructor[0]])

                writer.writerow([])

                writer.writerow(["Courses"])
                writer.writerow(["Course ID", "Course Name", "Instructor", "Enrolled Students"])
                cursor.execute("SELECT * FROM courses")
                for course in cursor.fetchall():
                    instructor_name = cursor.execute("SELECT name FROM instructors WHERE instructor_id = ?", (course[2],)).fetchone()[0] if course[2] else "None"
                    cursor.execute("SELECT * FROM student_courses WHERE course_id = ?", (course[0],))
                    enrolled_students_names = ', '.join([s[0] for s in cursor.fetchall()])
                    writer.writerow([course[0], course[1], instructor_name, enrolled_students_names])

            QMessageBox.information(self, "Success", f"Data exported successfully to {file_path}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
