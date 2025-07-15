import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class StudentAttendance(Document):
    def validate(self):
        # Auto-fill academic year
        if not self.academic_year:
            today = nowdate()
            academic_year = frappe.db.get_value(
                "Academic Year",
                {
                    "start_date": ["<=", today],
                    "end_date": [">=", today]
                },
                "name"
            )
            if academic_year:
                self.academic_year = academic_year
            else:
                frappe.msgprint("No valid Academic Year found for today.")

        # Prevent duplicate attendance
        existing = frappe.db.exists(
            "Student Attendance",
            {
                "student": self.student,
                "date": self.date,
                "name": ["!=", self.name]
            }
        )

        if existing:
            frappe.throw(
                f"Attendance already marked for {self.student} on {self.date}."
            )