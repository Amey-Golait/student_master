import frappe
from frappe.model.document import Document

class Class(Document):
    def validate(self):
        if self.class_name:
            self.class_name = self.class_name.strip()

        # Optional: validate academic year dates
        if self.academic_year:
            ay = frappe.get_doc("Academic Year", self.academic_year)
            if ay.status == "Archived" and self.status == "Active":
                frappe.throw("Cannot assign Archived Academic Year to an Active Class.")
