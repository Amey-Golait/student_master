import frappe

def execute(filters=None):
    if not filters.get("student"):
        frappe.throw("Please select a Student")

    columns = [
        {"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "width": 120},
        {"label": "Exam Name", "fieldname": "exam_name", "fieldtype": "Data", "width": 150},
        {"label": "Marks Obtained", "fieldname": "marks_obtained", "fieldtype": "Int", "width": 120},
        {"label": "Total Marks", "fieldname": "total_marks", "fieldtype": "Int", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90}
    ]

    data = []
    subject_totals = {}

    # Fetch all exams across academic years/classes
    exams = frappe.get_all("Exam", fields=["name", "exam_name", "subject", "total_marks"], order_by="subject, exam_name")

    for exam in exams:
        result = frappe.get_all("Student Exam Result", filters={
            "parent": exam.name,
            "student": filters["student"]
        }, fields=["marks_obtained", "status"])

        if result:
            row = result[0]
            marks = row.marks_obtained if row.status != "Absent" else None

            data.append({
                "subject": exam.subject,
                "exam_name": exam.exam_name,
                "marks_obtained": marks,
                "total_marks": exam.total_marks,
                "status": row.status
            })

            if exam.subject not in subject_totals:
                subject_totals[exam.subject] = {"marks_obtained": 0, "total_marks": 0}

            if row.status != "Absent":
                subject_totals[exam.subject]["marks_obtained"] += row.marks_obtained or 0
                subject_totals[exam.subject]["total_marks"] += exam.total_marks

    # Format subject-wise data and add totals
    subjectwise_data = []
    current_subject = None
    for row in data:
        if row["subject"] != current_subject:
            if current_subject:
                totals = subject_totals[current_subject]
                subjectwise_data.append({
                    "subject": f"{current_subject} Total",
                    "exam_name": "",
                    "marks_obtained": totals["marks_obtained"],
                    "total_marks": totals["total_marks"],
                    "status": ""
                })
            current_subject = row["subject"]
        subjectwise_data.append(row)

    # Add last subject's total
    if current_subject and current_subject in subject_totals:
        totals = subject_totals[current_subject]
        subjectwise_data.append({
            "subject": f"{current_subject} Total",
            "exam_name": "",
            "marks_obtained": totals["marks_obtained"],
            "total_marks": totals["total_marks"],
            "status": ""
        })

    # Grand Total
    grand_total_marks = sum(v["marks_obtained"] for v in subject_totals.values())
    grand_total_out_of = sum(v["total_marks"] for v in subject_totals.values())

    subjectwise_data.append({
        "subject": "Grand Total",
        "exam_name": "",
        "marks_obtained": grand_total_marks,
        "total_marks": grand_total_out_of,
        "status": ""
    })

    return columns, subjectwise_data
