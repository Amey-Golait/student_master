import frappe
from frappe.model.document import Document
from student_master.student_master.utils.send_exam_result_telegram import send_assignment_telegram

class Assignment(Document):
    def validate(self):
        if not self.academic_year:
            frappe.throw("Academic Year is required.")
        if not self.questions:
            frappe.throw("Questions field cannot be empty.")

def handle_on_submit(doc, method=None):
    try:
        frappe.logger().info(f"📤 Submitting Assignment: {doc.name}")
        send_assignment_telegram(doc.name)
    except Exception as e:
        frappe.log_error(f"Telegram Send Failed: {str(e)}", "Assignment Submit Hook")