from student import app,db

import student

from student.models import User
print("تم استيراد student بنجاح")
print(dir(student))



from student.models import (
    User,
    AcademicTerm,
    Course,
    CLO,
    Assessment,
    Question,
    Student,
    Enrollment,
    StudentQuestionResult,
    StudentAssessmentResult
)



if __name__ == "__main__":
    app.run(debug=True)