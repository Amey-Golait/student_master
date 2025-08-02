import frappe
from frappe.model.document import Document

class ClassEnrollment(Document):
    def validate(self):
        if not self.student or not self.class_link or not self.academic_year:
            frappe.throw("Student, Class, and Academic Year are mandatory.")

        if self.status == "Active":
            exists = frappe.db.exists(
                "Class Enrollment",
                {
                    "student": self.student,
                    "academic_year": self.academic_year,
                    "status": "Active",
                    "name": ["!=", self.name]
                }
            )
            if exists:
                frappe.throw(f"{self.student} is already actively enrolled in {self.academic_year}.")
