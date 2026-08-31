from student import db
from flask_login import UserMixin


# =========================================================
# USER / INSTRUCTOR
# =========================================================

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fname = db.Column(
        db.String(50),
        nullable=False
    )

    lname = db.Column(
        db.String(50),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="instructor"
    )

    # -----------------------------------------------------
    # Courses
    # -----------------------------------------------------

    courses = db.relationship(
        "Course",
        back_populates="instructor",
        lazy=True
    )

    def __repr__(self):

        return (
            f"User("
            f"'{self.username}', "
            f"'{self.email}', "
            f"'{self.role}')"
        )


# =========================================================
# ACADEMIC TERM
# =========================================================

class AcademicTerm(db.Model):

    __tablename__ = "academic_term"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    academic_year = db.Column(
        db.String(9),
        nullable=False
    )

    semester = db.Column(
        db.String(20),
        nullable=False
    )

    # -----------------------------------------------------
    # Courses
    # -----------------------------------------------------

    courses = db.relationship(
        "Course",
        back_populates="academic_term",
        lazy=True
    )

    # -----------------------------------------------------
    # Prevent duplicate academic terms
    # -----------------------------------------------------

    __table_args__ = (

        db.UniqueConstraint(
            "academic_year",
            "semester",
            name="unique_academic_term"
        ),

    )

    def __repr__(self):

        return (
            f"AcademicTerm("
            f"'{self.academic_year}', "
            f"'{self.semester}')"
        )


# =========================================================
# COURSE
# =========================================================

class Course(db.Model):

    __tablename__ = "course"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_code = db.Column(
        db.String(30),
        nullable=False
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # -----------------------------------------------------
    # Instructor
    # -----------------------------------------------------

    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    instructor = db.relationship(
        "User",
        back_populates="courses"
    )

    # -----------------------------------------------------
    # Academic Term
    # -----------------------------------------------------

    academic_term_id = db.Column(
        db.Integer,
        db.ForeignKey("academic_term.id"),
        nullable=False
    )

    academic_term = db.relationship(
        "AcademicTerm",
        back_populates="courses"
    )

    # -----------------------------------------------------
    # CLOs
    # -----------------------------------------------------

    clos = db.relationship(
        "CLO",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy=True
    )

    # -----------------------------------------------------
    # Assessments
    # -----------------------------------------------------

    assessments = db.relationship(
        "Assessment",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy=True
    )

    # -----------------------------------------------------
    # Enrollments
    # -----------------------------------------------------

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):

        return (
            f"Course("
            f"'{self.course_code}', "
            f"'{self.course_name}')"
        )


# =========================================================
# CLO
# =========================================================

class CLO(db.Model):

    __tablename__ = "clo"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # CLO Code
    #
    # Example:
    # CLO1
    # CLO2
    # CLO3
    # -----------------------------------------------------

    clo_code = db.Column(
        db.String(20),
        nullable=False
    )

    # -----------------------------------------------------
    # CLO Description
    # -----------------------------------------------------

    description = db.Column(
        db.Text,
        nullable=False
    )

    # -----------------------------------------------------
    # CLO Category
    # -----------------------------------------------------

    category = db.Column(
        db.String(50),
        nullable=False
    )

    # -----------------------------------------------------
    # Course
    # -----------------------------------------------------

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    course = db.relationship(
        "Course",
        back_populates="clos"
    )

    # -----------------------------------------------------
    # Questions
    #
    # Many-to-many relationship
    #
    # One CLO -> many questions
    # One Question -> many CLOs
    # -----------------------------------------------------

    questions = db.relationship(
        "Question",
        secondary="question_clo",
        back_populates="clos",
        lazy=True
    )

    # -----------------------------------------------------
    # Prevent duplicate CLO code inside same course
    # -----------------------------------------------------

    __table_args__ = (

        db.UniqueConstraint(
            "course_id",
            "clo_code",
            name="unique_clo_code_per_course"
        ),

    )

    def __repr__(self):

        return (
            f"CLO("
            f"'{self.clo_code}', "
            f"'{self.category}')"
        )


# =========================================================
# ASSESSMENT
# =========================================================

class Assessment(db.Model):

    __tablename__ = "assessment"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # Assessment Name
    #
    # Examples:
    # Midterm Exam
    # Final Exam
    # Quiz 1
    # Assignment 1
    # Project
    # -----------------------------------------------------

    name = db.Column(
        db.String(100),
        nullable=False
    )

    # -----------------------------------------------------
    # Assessment Type
    #
    # Examples:
    # Exam
    # Quiz
    # Assignment
    # Project
    # Practical
    # Other
    # -----------------------------------------------------

    assessment_type = db.Column(
        db.String(50),
        nullable=True
    )

    # -----------------------------------------------------
    # Description
    # -----------------------------------------------------

    description = db.Column(
        db.Text,
        nullable=True
    )

    # -----------------------------------------------------
    # Maximum Assessment Mark
    #
    # Example:
    # Midterm = 30
    # Final = 50
    # Quiz = 10
    # -----------------------------------------------------

    max_mark = db.Column(
        db.Float,
        nullable=False
    )

    # -----------------------------------------------------
    # Assessment Weight
    #
    # Example:
    # Midterm = 30%
    # Final = 40%
    # Quiz = 10%
    # -----------------------------------------------------

    weight = db.Column(
        db.Float,
        nullable=False
    )

    # -----------------------------------------------------
    # Course
    # -----------------------------------------------------

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    course = db.relationship(
        "Course",
        back_populates="assessments"
    )

    # -----------------------------------------------------
    # Questions
    #
    # Assessment CAN have zero questions.
    #
    # Questions can be:
    # - added manually
    # - imported from Excel
    # - edited
    # - deleted
    # -----------------------------------------------------

    questions = db.relationship(
        "Question",
        back_populates="assessment",
        cascade="all, delete-orphan",
        lazy=True
    )

    # -----------------------------------------------------
    # Student Assessment Results
    # -----------------------------------------------------

    results = db.relationship(
        "StudentAssessmentResult",
        back_populates="assessment",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):

        return (
            f"Assessment("
            f"'{self.name}', "
            f"{self.max_mark}, "
            f"{self.weight}%)"
        )


# =========================================================
# QUESTION
# =========================================================

class Question(db.Model):

    __tablename__ = "question"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # Question Name / Text
    #
    # This is the question text imported from Excel.
    # -----------------------------------------------------

    question_text = db.Column(
        db.Text,
        nullable=False
    )

    # -----------------------------------------------------
    # Question Mark
    #
    # Example:
    # Q1 = 5
    # Q2 = 10
    # Q3 = 15
    # -----------------------------------------------------

    max_mark = db.Column(
        db.Float,
        nullable=False
    )

    # -----------------------------------------------------
    # Assessment
    # -----------------------------------------------------

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessment.id"),
        nullable=False
    )

    assessment = db.relationship(
        "Assessment",
        back_populates="questions"
    )

    # -----------------------------------------------------
    # CLO Mapping
    #
    # Many-to-many relationship.
    #
    # Example:
    #
    # Q1 -> CLO1
    #
    # Q2 -> CLO1 + CLO2
    #
    # Q3 -> CLO1 + CLO2 + CLO3
    #
    # IMPORTANT:
    # We DO NOT store split marks here.
    # -----------------------------------------------------

    clos = db.relationship(
        "CLO",
        secondary="question_clo",
        back_populates="questions",
        lazy=True
    )

    # -----------------------------------------------------
    # Student Question Results
    # -----------------------------------------------------

    results = db.relationship(
        "StudentQuestionResult",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):

        return (
            f"Question("
            f"'{self.id}', "
            f"{self.max_mark})"
        )


# =========================================================
# QUESTION <-> CLO MAPPING
# =========================================================
#
# This table stores ONLY the relationship.
#
# It does NOT store:
# - split_mark
# - mark_per_clo
# - achievement
#
# Example:
#
# question_id | clo_id
# ------------|-------
#     1       |   1
#     1       |   2
#     2       |   1
#     3       |   2
#     3       |   3
#
# If Q1 = 10 marks and is mapped to CLO1 + CLO2:
#
# CLO1 contribution = 10 / 2
# CLO2 contribution = 10 / 2
#
# This is calculated later.
# =========================================================

question_clo = db.Table(

    "question_clo",

    db.Column(
        "question_id",
        db.Integer,
        db.ForeignKey(
            "question.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    db.Column(
        "clo_id",
        db.Integer,
        db.ForeignKey(
            "clo.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

)


# =========================================================
# STUDENT
# =========================================================

class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    fname = db.Column(
        db.String(50),
        nullable=False
    )

    lname = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    # -----------------------------------------------------
    # Enrollments
    # -----------------------------------------------------

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):

        return (
            f"Student("
            f"'{self.student_number}', "
            f"'{self.fname} {self.lname}')"
        )


# =========================================================
# ENROLLMENT
# =========================================================

class Enrollment(db.Model):

    __tablename__ = "enrollment"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # Student
    # -----------------------------------------------------

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # Course
    # -----------------------------------------------------

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    student = db.relationship(
        "Student",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    # -----------------------------------------------------
    # Prevent duplicate enrollment
    # -----------------------------------------------------

    __table_args__ = (

        db.UniqueConstraint(
            "student_id",
            "course_id",
            name="unique_student_course"
        ),

    )

    def __repr__(self):

        return (
            f"Enrollment("
            f"Student={self.student_id}, "
            f"Course={self.course_id})"
        )


# =========================================================
# STUDENT QUESTION RESULT
# =========================================================
#
# Stores the actual mark obtained by a student for a
# particular question.
#
# Example:
#
# Question maximum = 10
# Student got = 8
#
# Stored:
# mark = 8
#
# We DO NOT store:
# CLO1 = 4
# CLO2 = 4
#
# These are calculated later.
# =========================================================

class StudentQuestionResult(db.Model):

    __tablename__ = "student_question_result"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # Enrollment
    # -----------------------------------------------------

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # Question
    # -----------------------------------------------------

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # Student Mark
    # -----------------------------------------------------

    mark = db.Column(
        db.Float,
        nullable=False
    )

    enrollment = db.relationship(
        "Enrollment",
        backref="question_results"
    )

    question = db.relationship(
        "Question",
        back_populates="results"
    )

    # -----------------------------------------------------
    # One result per student/question
    # -----------------------------------------------------

    __table_args__ = (

        db.UniqueConstraint(
            "enrollment_id",
            "question_id",
            name="unique_student_question_result"
        ),

    )

    def __repr__(self):

        return (
            f"StudentQuestionResult("
            f"'{self.enrollment_id}', "
            f"'{self.question_id}', "
            f"'{self.mark}')"
        )


# =========================================================
# STUDENT ASSESSMENT RESULT
# =========================================================
#
# Stores the total mark obtained by a student in an
# assessment.
#
# Example:
#
# Assessment = 30
# Student got = 24
#
# Stored:
# mark = 24
#
# CLO achievement is calculated later.
# =========================================================

class StudentAssessmentResult(db.Model):

    __tablename__ = "student_assessment_result"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # Enrollment
    # -----------------------------------------------------

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # Assessment
    # -----------------------------------------------------

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # Student Assessment Mark
    # -----------------------------------------------------

    mark = db.Column(
        db.Float,
        nullable=False
    )

    enrollment = db.relationship(
        "Enrollment",
        backref="assessment_results"
    )

    assessment = db.relationship(
        "Assessment",
        back_populates="results"
    )

    # -----------------------------------------------------
    # One result per student/assessment
    # -----------------------------------------------------

    __table_args__ = (

        db.UniqueConstraint(
            "enrollment_id",
            "assessment_id",
            name="unique_student_assessment_result"
        ),

    )

    def __repr__(self):

        return (
            f"StudentAssessmentResult("
            f"'{self.enrollment_id}', "
            f"'{self.assessment_id}', "
            f"'{self.mark}')"
        )