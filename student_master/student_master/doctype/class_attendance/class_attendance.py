# Copyright (c) 2025, Amey Golait and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ClassAttendance(Document):
	pass
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

        student_name = student_doc.full_name if hasattr(student_doc, "full_name") else student_doc.name

        results.append({
            "student": student_id,
            "student_name": student_name
        })

    frappe.msgprint(f"Returning {len(results)} students")
    return results
