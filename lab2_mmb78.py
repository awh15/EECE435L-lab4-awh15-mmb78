def is_valid_email(email):
    if "@" in email and "." in email.split("@")[1]:
        return True
    return False

def is_non_negative_age(age):
    return isinstance(age, int) and age >= 0

class Person:
    def __init__(self, name, age, email):
        if not is_valid_email(email):
            raise ValueError("Invalid format for email.")
        if not is_non_negative_age(age):
            raise ValueError("Invalid age value.")

        self.name = name
        self.age = age
        self.__email = email  # Private

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if not is_valid_email(email):
            raise ValueError("Invalid format for email.")
        self.__email = email

    def introduce(self):
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["email"])

class Student(Person):
    def __init__(self, name, age, email, student_id, registered_courses=None):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses is not None else []

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "student_id": self.student_id,
            "registered_courses": [course.course_id for course in self.registered_courses]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        student = cls(
            name=data["name"],
            age=data["age"],
            email=data["email"],
            student_id=data["student_id"],
            registered_courses=[course_id for course_id in data["registered_courses"]]
        )
        return student


class Instructor(Person):
    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.course_id for course in self.assigned_courses]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        instructor = cls(
            name=data["name"],
            age=data["age"],
            email=data["email"],
            instructor_id=data["instructor_id"],
            assigned_courses=[Course(course_id) for course_id in data["assigned_courses"]]
        )
        return instructor


class Course:
    def __init__(self, course_id, course_name, instructor, enrolled_students=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students if enrolled_students is not None else []  

    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor": self.instructor.to_dict() if self.instructor else None,
            "enrolled_students": [student.to_dict() for student in self.enrolled_students]  
        }

    @classmethod
    def from_dict(cls, data):
        instructor_data = data.get("instructor")
        instructor = Instructor.from_dict(instructor_data) if instructor_data else None
        enrolled_students = [Student.from_dict(student_data) for student_data in data.get("enrolled_students", [])]
        return cls(
            course_id=data["course_id"],
            course_name=data["course_name"],
            instructor=instructor,
            enrolled_students=enrolled_students  
        )

