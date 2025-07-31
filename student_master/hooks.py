app_name = "student_master"
app_title = "student_master"
app_publisher = "Amey Golait"
app_description = "Student Management System"
app_email = "ameygolait123@gmail.com"
app_license = "mit"
fixtures = [{"dt": "DocType", "filters": [["name", "in", ["Student", "Guardian Detail"]]]}]

doc_events = {
    "Assignment": {
        "on_submit": "student_master.student_master.doctype.assignment.assignment.handle_on_submit"
    },
    "Assignment Submission": {
        "on_submit": "student_master.student_master.doctype.assignment_submission.assignment_submission.handle_on_submit"
    },
    "Exam": {
        "on_submit": "student_master.student_master.doctype.exam.exam.handle_on_submit"
    },
    "Assignment Review": {
        "on_submit": "student_master.student_master.doctype.assignment_review.assignment_review.handle_on_submit"
    }
}

