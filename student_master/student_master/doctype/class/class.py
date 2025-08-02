import frappe
from frappe.model.document import Document

class Class(Document):
    def validate(self):
        if self.class_name:
            self.class_name = self.class_name.strip()

        if self.class_name and self.section and self.academic_year:
            self.title = f"{self.class_name}-{self.section} - {self.academic_year}"

        if self.academic_year:
            ay = frappe.get_doc("Academic Year", self.academic_year)
            if ay.status == "Archived" and self.status == "Active":
                frappe.throw("Cannot assign Archived Academic Year to an Active Class.")
