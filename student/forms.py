from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    FloatField,
    FileField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
    NumberRange,
    Optional
)

from flask_wtf.file import (
    FileAllowed,
    FileRequired
)

from student.models import (
    User,
    Student
)


# =========================================================
# REGISTRATION FORM
# =========================================================

class RegistrationForm(FlaskForm):

    fname = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=2, max=25)
        ]
    )

    lname = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=2, max=25)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=2, max=25)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("instructor", "Instructor"),
            ("admin", "Admin")
        ],
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
                r"(?=.*[@$!%*?&_])"
                r"[A-Za-z\d@$!%*?&_]{8,32}$",
                message=(
                    "Password must contain at least one uppercase letter, "
                    "one lowercase letter, one number, and one special character."
                )
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Sign Up"
    )

    # -----------------------------------------------------
    # USERNAME VALIDATION
    # -----------------------------------------------------

    def validate_username(self, username):

        username_value = username.data.strip()

        user = User.query.filter_by(
            username=username_value
        ).first()

        if user:

            raise ValidationError(
                "Username already exists. Please choose another one."
            )

    # -----------------------------------------------------
    # EMAIL VALIDATION
    # -----------------------------------------------------

    def validate_email(self, email):

        email_value = email.data.strip().lower()

        user = User.query.filter_by(
            email=email_value
        ).first()

        if user:

            raise ValidationError(
                "Email already exists. Please choose another one."
            )


# =========================================================
# LOGIN FORM
# =========================================================

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField(
        "Remember Me"
    )

    submit = SubmitField(
        "Log In"
    )


# =========================================================
# COURSE FORM
# =========================================================

class CourseForm(FlaskForm):

    course_code = StringField(
        "Course Code",
        validators=[
            DataRequired(),
            Length(min=2, max=30)
        ],
        render_kw={
            "placeholder": "Example: CS101"
        }
    )

    course_name = StringField(
        "Course Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ],
        render_kw={
            "placeholder": "Example: Introduction to Programming"
        }
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional()
        ],
        render_kw={
            "placeholder": "Enter course description..."
        }
    )

    academic_year = SelectField(
        "Academic Year",
        choices=[],
        validators=[
            DataRequired()
        ]
    )

    semester = SelectField(
        "Semester",
        choices=[
            ("First", "First Semester"),
            ("Second", "Second Semester"),
            ("Summer", "Summer Semester")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Save Course"
    )


# =========================================================
# CLO FORM
# =========================================================

class CLOForm(FlaskForm):

    clo_code = StringField(
        "CLO Code",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20
            )
        ],
        render_kw={
            "placeholder": "Example: CLO1"
        }
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(),
            Length(min=5)
        ],
        render_kw={
            "placeholder": "Enter CLO description..."
        }
    )

    category = SelectField(
        "Category",
        choices=[
            (
                "Knowledge & Understanding",
                "Knowledge & Understanding"
            ),
            (
                "Professional Skills",
                "Professional Skills"
            ),
            (
                "Competences",
                "Competences"
            )
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Save CLO"
    )


# =========================================================
# ASSESSMENT FORM
# =========================================================

class AssessmentForm(FlaskForm):

    name = StringField(
        "Assessment Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=100
            )
        ],
        render_kw={
            "placeholder": "Example: Quiz 1"
        }
    )

    assessment_type = SelectField(
        "Assessment Type",
        choices=[
            (
                "Participation",
                "Participation"
            ),
            (
                "Quiz",
                "Quiz"
            ),
            (
                "Midterm",
                "Midterm Exam"
            ),
            (
                "Final",
                "Final Exam"
            )
        ],
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional()
        ],
        render_kw={
            "placeholder": "Enter assessment description..."
        }
    )

    max_mark = FloatField(
        "Total Marks",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="Assessment marks must be greater than 0."
            )
        ],
        render_kw={
            "placeholder": "Example: 30"
        }
    )

    weight = FloatField(
        "Weight (%)",
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=100,
                message="Weight must be between 0 and 100."
            )
        ],
        render_kw={
            "placeholder": "Example: 30"
        }
    )

    submit = SubmitField(
        "Save Assessment"
    )


# =========================================================
# QUESTION FORM
# =========================================================

class QuestionForm(FlaskForm):

    question_text = TextAreaField(
        "Question",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=2000
            )
        ],
        render_kw={
            "placeholder": "Enter question..."
        }
    )

    max_mark = FloatField(
        "Question Marks",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="Question marks must be greater than 0."
            )
        ],
        render_kw={
            "placeholder": "Example: 5"
        }
    )

    submit = SubmitField(
        "Save Question"
    )


# =========================================================
# QUESTION CLO MAPPING FORM
# =========================================================

class QuestionCLOForm(FlaskForm):

    clos = SelectField(
        "CLO",
        choices=[],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Save CLO Mapping"
    )


# =========================================================
# EXCEL QUESTION UPLOAD FORM
# =========================================================

class QuestionExcelUploadForm(FlaskForm):

    file = FileField(
        "Questions Excel File",
        validators=[
            FileRequired(
                message="Please select an Excel file."
            ),
            FileAllowed(
                [
                    "xlsx",
                    "xlsm"
                ],
                "Only Excel files (.xlsx or .xlsm) are allowed."
            )
        ]
    )

    submit = SubmitField(
        "Upload Questions"
    )


# =========================================================
# STUDENT FORM
# =========================================================
#
# Used for:
# - Add Student
# - Edit Student
#
# Input:
# - University ID
# - Full Student Name
#
# Example:
# Ahmad Mohammad Ali
#
# fname = Ahmad
# lname = Mohammad Ali
# =========================================================

class StudentForm(FlaskForm):

    student_number = StringField(
        "University ID",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=30
            )
        ],
        render_kw={
            "placeholder": "Example: 20230001"
        }
    )

    student_name = StringField(
        "Student Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=100
            )
        ],
        render_kw={
            "placeholder": "Example: Ahmad Mohammad"
        }
    )

    submit = SubmitField(
        "Save Student"
    )


# =========================================================
# STUDENT EXCEL IMPORT FORM
# =========================================================
#
# Expected Excel:
#
# University ID | Student Name
#
# =========================================================

class StudentExcelUploadForm(FlaskForm):

    file = FileField(
        "Students Excel File",
        validators=[
            FileRequired(
                message="Please select an Excel file."
            ),
            FileAllowed(
                [
                    "xlsx",
                    "xlsm"
                ],
                "Only Excel files (.xlsx or .xlsm) are allowed."
            )
        ]
    )

    submit = SubmitField(
        "Import Students"
    )


# =========================================================
# STUDENT MARKS EXCEL IMPORT FORM
# =========================================================
#
# Used for uploading marks for a specific Assessment.
#
# Expected Excel:
#
# University ID | Student Name | Q1 | Q2 | Q3 | Q4
#
# Example:
#
# 20230001 | Ahmad Mohammad | 8 | 7 | 9 | 5
# 20230002 | Sara Ali      | 9 | 6 | 8 | 4
#
# Q1, Q2, Q3 ... correspond to the questions
# inside the selected assessment.
#
# =========================================================

class StudentMarksExcelUploadForm(FlaskForm):

    file = FileField(
        "Student Marks Excel File",
        validators=[
            FileRequired(
                message="Please select an Excel file."
            ),
            FileAllowed(
                [
                    "xlsx",
                    "xlsm"
                ],
                "Only Excel files (.xlsx or .xlsm) are allowed."
            )
        ]
    )

    submit = SubmitField(
        "Upload Student Marks"
    )