import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
from lab2_mmb78 import Student, Instructor, Course
from db_mmb78 import *

# Sample data storage
courses = []
students = []
instructors = []

create_tables()
root = tk.Tk()
root.title("School Management System")
root.geometry("1300x700")


def submit_student():
    """
    Handles the submission of a student entry.

    This function collects the student data from input fields and stores the
    student in the database. It validates the inputs before proceeding.
    """
    name = entry_student_name.get()
    age = entry_student_age.get()
    email = entry_student_email.get()
    student_id = entry_student_id.get()

    if name == "" or age == "" or email == "" or student_id == "":
        messagebox.showerror("Input Error", "All fields must be filled out")
        return

    new_student = Student(name=name, age=int(age), email=email, student_id=student_id)
    add_student(new_student)
    #students.append(new_student)
    update_dropdowns()
    
    messagebox.showinfo("Submission Successful", f"Student {name} has been added!")
    display_records()

    entry_student_name.delete(0, tk.END)
    entry_student_age.delete(0, tk.END)
    entry_student_email.delete(0, tk.END)
    entry_student_id.delete(0, tk.END)


def submit_instructor():
    """
    Handles the submission of an instructor entry.

    This function collects the instructor data from input fields and stores the
    instructor in the database. It validates the inputs before proceeding.
    """
    name = entry_instructor_name.get()
    age = entry_instructor_age.get()
    email = entry_instructor_email.get()
    instructor_id = entry_instructor_id.get()

    if name == "" or age == "" or email == "" or instructor_id == "":
        messagebox.showerror("Input Error", "All fields must be filled out")
        return

    new_instructor = Instructor(name=name, age=int(age), email=email, instructor_id=instructor_id)
    #instructors.append(new_instructor)
    add_instructor(new_instructor)
    update_dropdowns()
    
    messagebox.showinfo("Submission Successful", f"Instructor {name} has been added!")
    display_records()

    entry_instructor_name.delete(0, tk.END)
    entry_instructor_age.delete(0, tk.END)
    entry_instructor_email.delete(0, tk.END)
    entry_instructor_id.delete(0, tk.END)


def submit_course():
    """
    Handles the submission of a course entry.

    This function collects the course data from input fields, validates the inputs, and stores the
    course in the database. It checks for the existence of an instructor before proceeding.
    """
    course_id = entry_course_id.get()
    course_name = entry_course_name.get()
    instructor_name = entry_course_instructor.get()

    if not course_id or not course_name or not instructor_name:
        messagebox.showerror("Input Error", "All fields must be filled out")
        return

    selected_instructor = get_instructor_by_name(instructor_name)

    if not selected_instructor:
        messagebox.showerror("Input Error", "Instructor not found in the database")
        return

    new_course = Course(course_id=course_id, course_name=course_name, instructor=selected_instructor)
    
    add_course(new_course)

    update_dropdowns()
    messagebox.showinfo("Submission Successful", f"Course '{course_name}' has been added!")

    entry_course_id.delete(0, tk.END)
    entry_course_name.delete(0, tk.END)
    entry_course_instructor.delete(0, tk.END)

    display_records()


def update_dropdowns():
    """
    Updates dropdowns for courses, students, and instructors.

    This function fetches the latest data from the database and updates the
    dropdown menus in the UI.
    """
    courses = get_all_courses()
    students = get_all_students()
    instructors = get_all_instructors()

    course_menu = course_dropdown["menu"]
    course_menu.delete(0, "end")
    course_assign_menu = course_dropdown_assign["menu"]
    course_assign_menu.delete(0, "end")
    for course in courses:
        course_menu.add_command(label=course.course_name, command=lambda value=course.course_name: course_var.set(value))
        course_assign_menu.add_command(label=course.course_name, command=lambda value=course.course_name: course_var.set(value))

    student_menu = student_dropdown["menu"]
    student_menu.delete(0, "end")
    for student in students:
        student_menu.add_command(label=student.name, command=lambda value=student.name: student_var.set(value))

    instructor_menu = instructor_dropdown["menu"]
    instructor_menu.delete(0, "end")
    for instructor in instructors:
        instructor_menu.add_command(label=instructor.name, command=lambda value=instructor.name: instructor_var.set(value))





def register_student():
    """
    Registers a student to a selected course.

    This function allows a student to be registered for a course by selecting
    both the student and the course from dropdowns. The registration is stored
    in the database.
    """
    student_name = student_var.get()
    course_name = course_var.get()

    if not student_name or not course_name:
        messagebox.showerror("Input Error", "Please select both student and course")
        return

    selected_student = next((s for s in get_all_students() if s.name == student_name), None)
    selected_course = next((c for c in get_all_courses() if c.course_name == course_name), None)

    if not selected_student or not selected_course:
        messagebox.showerror("Error", "Invalid student or course selection")
        return

    enroll_student(selected_student.student_id, selected_course.course_id)
    
    messagebox.showinfo("Registration Successful", f"Student {student_name} has been registered for {course_name}")

    student_var.set('')
    course_var.set('')

    display_records()  



def assign_instructor():
    """
    Assigns an instructor to a selected course.

    This function allows an instructor to be assigned to a course by selecting
    both the instructor and the course from dropdowns. The assignment is stored
    in the database.
    """
    instructor_name = instructor_var.get()
    course_name = course_var.get()

    if not instructor_name or not course_name:
        messagebox.showerror("Input Error", "Please select both instructor and course")
        return

    selected_instructor = next((i for i in get_all_instructors() if i.name == instructor_name), None)
    selected_course = next((c for c in get_all_courses() if c.course_name == course_name), None)

    if not selected_instructor or not selected_course:
        messagebox.showerror("Error", "Invalid instructor or course selection")
        return

    selected_course.instructor = selected_instructor  
    update_course(selected_course)  

    messagebox.showinfo("Assignment Successful", f"Instructor {instructor_name} has been assigned to {course_name}")

    instructor_var.set('')
    course_var.set('')

    display_records() 


def edit_record():
    """
    Handles the editing of a selected record.

    This function allows editing of the student, instructor, or course record
    selected from the TreeView widget. The changes are saved to the database.
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to edit.")
        return

    values = tree.item(selected_item, "values")
    record_type, record_id, record_name = values[0], values[1], values[2]

    popup = tk.Toplevel(root)
    popup.title(f"Edit {record_type} {record_name}")

    if record_type == "Student":
        student = get_student_by_id(record_id)

        tk.Label(popup, text="Name").pack()
        name_entry = tk.Entry(popup)
        name_entry.pack()
        name_entry.insert(0, student.name)

        tk.Label(popup, text="Age").pack()
        age_entry = tk.Entry(popup)
        age_entry.pack()
        age_entry.insert(0, student.age)

        tk.Label(popup, text="Email").pack()
        email_entry = tk.Entry(popup)
        email_entry.pack()
        email_entry.insert(0, student.get_email())

        def save_changes():
            student.name = name_entry.get()
            student.age = int(age_entry.get())
            student.set_email(email_entry.get())

            update_student(student)

            display_records()
            popup.destroy()

        tk.Button(popup, text="Save", command=save_changes).pack()

    elif record_type == "Instructor":
        instructor = get_instructor_by_id(record_id)

        tk.Label(popup, text="Name").pack()
        name_entry = tk.Entry(popup)
        name_entry.pack()
        name_entry.insert(0, instructor.name)

        tk.Label(popup, text="Age").pack()
        age_entry = tk.Entry(popup)
        age_entry.pack()
        age_entry.insert(0, instructor.age)

        tk.Label(popup, text="Email").pack()
        email_entry = tk.Entry(popup)
        email_entry.pack()
        email_entry.insert(0, instructor.get_email())

        def save_changes():
            instructor.name = name_entry.get()
            instructor.age = int(age_entry.get())
            instructor.set_email(email_entry.get())

            update_instructor(instructor)

            display_records()
            popup.destroy()

        tk.Button(popup, text="Save", command=save_changes).pack()

    elif record_type == "Course":
        course = get_course_by_id(record_id)

        tk.Label(popup, text="Course Name").pack()
        course_name_entry = tk.Entry(popup)
        course_name_entry.pack()
        course_name_entry.insert(0, course.course_name)

        tk.Label(popup, text="Instructor").pack()
        instructor_name_entry = tk.Entry(popup)
        instructor_name_entry.pack()
        instructor_name_entry.insert(0, course.instructor.name)

        def save_changes():
            course.course_name = course_name_entry.get()
            selected_instructor = get_instructor_by_name(instructor_name_entry.get())  
            if selected_instructor:
                course.instructor = selected_instructor

                update_course(course)
            else:
                messagebox.showerror("Error", "Instructor not found")
                return

            display_records()
            popup.destroy()

        tk.Button(popup, text="Save", command=save_changes).pack()


def delete_record():
    """
    Deletes a selected record from the system.

    This function deletes a student, instructor, or course record after confirming the action.
    """    
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    values = tree.item(selected_item, "values")
    record_type, record_id = values[0], values[1]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {record_type}?")
    if not confirm:
        return

    if record_type == "Student":
        delete_student(record_id)
    elif record_type == "Instructor":
        delete_instructor(record_id)
    elif record_type == "Course":
        delete_course(record_id)

    display_records()

def save_data():
    """
    A placeholder for the save data function, currently unused.

    This function is a placeholder and does not perform any actual saving functionality.
    """

    messagebox.showinfo("OOPS", "this button is useless now")


def load_data():
    """
    A placeholder for the load data function, currently unused.

    This function is a placeholder and does not perform any actual loading functionality.
    """
    messagebox.showinfo("OOPS", "this button is useless now")

    
def search_records():
    """
    Searches for records based on the query.

    This function performs a search on students, instructors, and courses based on the input in the search field.
    """
    query = search_entry.get().lower()

    for item in tree.get_children():
        tree.delete(item)

    students = get_all_students()
    for student in students:
        if query in student.name.lower():
            tree.insert("", "end", values=("Student", student.student_id, student.name, student.age, student.get_email()))

    instructors = get_all_instructors()
    for instructor in instructors:
        if query in instructor.name.lower():
            tree.insert("", "end", values=("Instructor", instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))

    courses = get_all_courses()
    for course in courses:
        if query in course.course_name.lower():
            tree.insert("", "end", values=("Course", course.course_id, course.course_name, course.instructor.name, ", ".join([s.name for s in course.enrolled_students])))


def display_records():
    """
    Displays all records in the TreeView widget.

    This function fetches the latest records from the database and displays them in the UI.
    """
    update_dropdowns()

    for item in tree.get_children():
        tree.delete(item)

    students = get_all_students()
    for student in students:
        tree.insert("", "end", values=("Student", student.student_id, student.name, student.age, student.get_email()))

    instructors = get_all_instructors()
    for instructor in instructors:
        tree.insert("", "end", values=("Instructor", instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))

    courses = get_all_courses()
    for course in courses:
        # Fetch enrolled students for each course
        enrolled_students = get_enrollments_for_course(course.course_id)
        enrolled_students_names = ", ".join([student.name for student in enrolled_students])
        
        tree.insert("", "end", values=(
            "Course", 
            course.course_id, 
            course.course_name, 
            course.instructor.name, 
            enrolled_students_names if enrolled_students else "No students enrolled"
        ))


    
# Create Treeview for displaying records
columns = ("Type", "ID", "Name", "Age/Instructor", "Email/Students")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(2, weight=1)

# Creating the UI forms
student_frame = tk.LabelFrame(root, text="Add Student", padx=10, pady=10)
student_frame.grid(row=0, column=0, padx=10, pady=10)
tk.Label(student_frame, text="Name").pack()
entry_student_name = tk.Entry(student_frame)
entry_student_name.pack()
tk.Label(student_frame, text="Age").pack()
entry_student_age = tk.Entry(student_frame)
entry_student_age.pack()
tk.Label(student_frame, text="Email").pack()
entry_student_email = tk.Entry(student_frame)
entry_student_email.pack()
tk.Label(student_frame, text="Student ID").pack()
entry_student_id = tk.Entry(student_frame)
entry_student_id.pack()
tk.Button(student_frame, text="Submit", command=submit_student).pack()

instructor_frame = tk.LabelFrame(root, text="Add Instructor", padx=10, pady=10)
instructor_frame.grid(row=1, column=0, padx=10, pady=10)
tk.Label(instructor_frame, text="Name").pack()
entry_instructor_name = tk.Entry(instructor_frame)
entry_instructor_name.pack()
tk.Label(instructor_frame, text="Age").pack()
entry_instructor_age = tk.Entry(instructor_frame)
entry_instructor_age.pack()
tk.Label(instructor_frame, text="Email").pack()
entry_instructor_email = tk.Entry(instructor_frame)
entry_instructor_email.pack()
tk.Label(instructor_frame, text="Instructor ID").pack()
entry_instructor_id = tk.Entry(instructor_frame)
entry_instructor_id.pack()
tk.Button(instructor_frame, text="Submit", command=submit_instructor).pack()

course_frame = tk.LabelFrame(root, text="Add Course", padx=10, pady=10)
course_frame.grid(row=2, column=0, padx=10, pady=10)
tk.Label(course_frame, text="Course ID").pack()
entry_course_id = tk.Entry(course_frame)
entry_course_id.pack()
tk.Label(course_frame, text="Course Name").pack()
entry_course_name = tk.Entry(course_frame)
entry_course_name.pack()
tk.Label(course_frame, text="Instructor Name").pack()
entry_course_instructor = tk.Entry(course_frame)
entry_course_instructor.pack()
tk.Button(course_frame, text="Submit", command=submit_course).pack()

registration_frame = tk.LabelFrame(root, text="Register Student to Course", padx=10, pady=10)
registration_frame.grid(row=0, column=1, padx=10, pady=10)
tk.Label(registration_frame, text="Select Student").pack()
student_var = tk.StringVar(root)
student_dropdown = tk.OptionMenu(registration_frame, student_var, [])
student_dropdown.pack()
tk.Label(registration_frame, text="Select Course").pack()
course_var = tk.StringVar(root)
course_dropdown = tk.OptionMenu(registration_frame, course_var, [])
course_dropdown.pack()
tk.Button(registration_frame, text="Register", command=register_student).pack()

assignment_frame = tk.LabelFrame(root, text="Assign Instructor to Course", padx=10, pady=10)
assignment_frame.grid(row=1, column=1, padx=10, pady=10)
tk.Label(assignment_frame, text="Select Instructor").pack()
instructor_var = tk.StringVar(root)
instructor_dropdown = tk.OptionMenu(assignment_frame, instructor_var, [])
instructor_dropdown.pack()
tk.Label(assignment_frame, text="Select Course").pack()
course_dropdown_assign = tk.OptionMenu(assignment_frame, course_var, [])
course_dropdown_assign.pack()
tk.Button(assignment_frame, text="Assign", command=assign_instructor).pack()

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")
tk.Button(button_frame, text="Edit", command=edit_record).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete", command=delete_record).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Save", command=save_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Load", command=load_data).pack(side=tk.LEFT, padx=5)

search_frame = tk.Frame(root)
search_frame.grid(row=2, column=1, padx=10, pady=10)
tk.Label(search_frame, text="Search by Name:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)
tk.Button(search_frame, text="Search", command=search_records).pack(side=tk.LEFT, padx=5)


display_records()
root.mainloop()
