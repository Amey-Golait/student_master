import frappe
from frappe.model.document import Document

class AcademicYear(Document):
    def validate(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            frappe.throw("End Date must be after Start Date.")
