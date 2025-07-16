import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    class_link = filters.get("class_link")
    academic_year = filters.get("academic_year")

    if not class_link or not academic_year:
        frappe.throw("Please select both Class and Academic Year.")

    # Get all exams for selected class/year
    exams = frappe.get_all("Exam", filters={
        "class_link": class_link,
        "academic_year": academic_year
    }, fields=["name", "subject"])

    subject_map = {}
    for exam in exams:
        subject_map.setdefault(exam.subject, []).append(exam.name)

    subjects = sorted(subject_map.keys())

    # Fetch scores
    student_scores = {}

    for subject in subjects:
        for exam_name in subject_map[subject]:
            results = frappe.get_all("Student Exam Result", filters={
                "parent": exam_name
            }, fields=["student", "student_name", "status", "marks_obtained"])

            for res in results:
                sid = res.student
                if sid not in student_scores:
                    student_scores[sid] = {
                        "student_name": res.student_name,
                        "marks": {},
                        "total": 0,
                        "count": 0
                    }

                marks = flt(res.marks_obtained) if res.status == "Present" else 0
                student_scores[sid]["marks"][subject] = marks
                student_scores[sid]["total"] += marks
                student_scores[sid]["count"] += 1

    # Build data rows
    data = []
    for sid, info in student_scores.items():
        row = [info["student_name"]]
        for subject in subjects:
            row.append(info["marks"].get(subject, 0))
        total = info["total"]
        average = round(total / info["count"], 2) if info["count"] else 0
        row += [total, average]
        data.append(row)

    # Sort by total descending and assign rank
    data.sort(key=lambda x: x[-2], reverse=True)
    for i, row in enumerate(data):
        row.append(i + 1)

    # Column definitions
    columns = [{"label": "Student", "fieldtype": "Data", "width": 200}]
    columns += [{"label": subject, "fieldtype": "Float", "width": 120} for subject in subjects]
    columns += [
        {"label": "Total", "fieldtype": "Float", "width": 100},
        {"label": "Average", "fieldtype": "Float", "width": 100},
        {"label": "Rank", "fieldtype": "Int", "width": 80}
    ]

    return columns, data
