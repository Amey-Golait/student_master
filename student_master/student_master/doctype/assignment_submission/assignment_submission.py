import frappe
from frappe.model.document import Document
from student_master.student_master.utils.send_exam_result_telegram import send_assignment_submission_telegram

class AssignmentSubmission(Document):
    pass

def handle_on_submit(doc, method=None):
    print("handle_on_submit triggered for", doc.name)
    try:
        send_assignment_submission_telegram(doc.name)
    except Exception as e:
        frappe.log_error(f"Telegram Send Failed: {str(e)}", "Assignment Submission Hook")
