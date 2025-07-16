# Copyright (c) 2025, Amey Golait and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
@frappe.whitelist()
def get_students_from_class(class_link, academic_year):
    frappe.msgprint(f"Getting students for: {class_link} ({academic_year})")

    enrollments = frappe.get_all(
        'Class Enrollment',
        filters={
            'class_link': class_link,
            'academic_year': academic_year
        },
        fields=['student']
    )

    frappe.msgprint(f"Enrollments found: {len(enrollments)}")

    results = []
    for e in enrollments:
        student_id = e.get("student")
        if not student_id:
            continue

        student_doc = frappe.get_doc("Student", student_id)

        student_name = getattr(student_doc, "full_name", student_doc.name)

        results.append({
            "student": student_id,
            "student_name": student_name
        })

    frappe.msgprint(f"Returning {len(results)} students")
    return results
