# Copyright (c) 2025, Amey Golait and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from datetime import datetime
from student_master.student_master.utils.send_exam_result_telegram import send_assignment_review_telegram

class AssignmentReview(Document):
	pass
@frappe.whitelist()
def get_submitted_assignments(assignment_review_name):
    review_doc = frappe.get_doc("Assignment Review", assignment_review_name)
    if not review_doc.assignment:
        frappe.throw("Please select an Assignment first.")

    assignment = frappe.get_doc("Assignment", review_doc.assignment)

    # ⚠️ Due date check disabled for testing
    # from datetime import datetime
    # if assignment.due_date > datetime.strptime(nowdate(), '%Y-%m-%d').date():
    #     frappe.throw("Submissions can only be reviewed after the due date.")

    # Clear old rows
    review_doc.review_table = []

    # Fetch all submissions with correct field
    submissions = frappe.get_all("Assignment Submission", 
        filters={"assignment": review_doc.assignment},
        fields=["student", "assignment_pdf"]  # corrected fieldname
    )

    for sub in submissions:
        review_doc.append("review_table", {
            "student": sub.student,
            "attachment": sub.assignment_pdf  # set into review_entry's 'attachment'
        })

    review_doc.save()
    return {"count": len(submissions)}


def handle_on_submit(doc, method=None):
    print("handle_on_submit triggered for", doc.name)
    try:
        send_assignment_review_telegram(doc.name)
    except Exception as e:
        frappe.log_error(f"Telegram Send Failed: {str(e)}", "Assignment Review Hook")

# get submission button only works after student due date
# this code is for real testing Submissions can only be reviewed after the due date.


# # Copyright (c) 2025, Amey Golait and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe.utils import nowdate
# from datetime import datetime
# from student_master.student_master.utils.send_exam_result_telegram import send_assignment_review_telegram

# class AssignmentReview(Document):
# 	pass

# @frappe.whitelist()
# def get_submitted_assignments(assignment_review_name):
#     review_doc = frappe.get_doc("Assignment Review", assignment_review_name)
#     if not review_doc.assignment:
#         frappe.throw("Please select an Assignment first.")

#     assignment = frappe.get_doc("Assignment", review_doc.assignment)

#     # Convert nowdate() string to date object
#     if assignment.due_date > datetime.strptime(nowdate(), '%Y-%m-%d').date():
#         frappe.throw("Submissions can only be reviewed after the due date.")

#     # Clear old rows
#     review_doc.review_table = []

#     # Fetch all submissions
#     submissions = frappe.get_all("Assignment Submission", 
#         filters={"assignment": review_doc.assignment},
#         fields=["student", "attachment"]
#     )

#     for sub in submissions:
#         review_doc.append("review_table", {
#             "student": sub.student,
#             "attachment": sub.attachment
#         })

#     review_doc.save()
#     return {"count": len(submissions)}


# def handle_on_submit(doc, method=None):
#     print("handle_on_submit triggered for", doc.name)
#     try:
#         send_assignment_review_telegram(doc.name)
#     except Exception as e:
#         frappe.log_error(f"Telegram Send Failed: {str(e)}", "Assignment Review Hook")
