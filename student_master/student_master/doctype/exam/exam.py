# exam.py

import frappe
from frappe.model.document import Document
from student_master.student_master.utils.send_exam_result_telegram import send_exam_result_telegram

class Exam(Document):
    def validate(self):
        if not self.total_marks or self.total_marks <= 0:
            frappe.throw("Total Marks must be greater than 0.")

        for row in self.students:
            if row.status == "Absent" and row.marks_obtained:
                frappe.throw(f"{row.student_name} is marked absent. Remove marks.")
            if row.status == "Present":
                if row.marks_obtained is None:
                    frappe.throw(f"Enter marks for {row.student_name}.")
                if row.marks_obtained > self.total_marks:
                    frappe.throw(f"{row.student_name}'s marks exceed Total Marks.")

# this function is used in hooks.py
def handle_on_submit(doc, method=None):
    try:
        frappe.logger().info(f"📤 Submitting Exam: {doc.name}")
        send_exam_result_telegram(doc.name)
    except Exception as e:
        frappe.log_error(f"Telegram Send Failed: {str(e)}", "Exam Submit Hook")

@frappe.whitelist()
def get_students_from_class(class_link, academic_year):
    # same as before
    ...
