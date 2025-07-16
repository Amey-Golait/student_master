import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    exam_id = filters.get("exam_id")
    class_link = filters.get("class_link")
    academic_year = filters.get("academic_year")

    if not (exam_id and class_link and academic_year):
        frappe.throw("Please select Exam, Class, and Academic Year.")

    # ✅ Get exam_name from selected exam
    base_exam = frappe.get_doc("Exam", exam_id)
    exam_name = base_exam.exam_name

    frappe.msgprint(f"Using exam_name: {exam_name}")

    # Fetch all exams under this test
    exams = frappe.get_all("Exam", filters={
        "exam_name": exam_name,
        "class_link": class_link,
        "academic_year": academic_year
    }, fields=["name", "subject"])

    if not exams:
        frappe.msgprint("No exams found for the selected test.")
        return [], []

    subject_map = {}
    for exam in exams:
        subject_map[exam.subject] = exam.name

    subjects = sorted(subject_map.keys())
    student_scores = {}

    for subject, exam_id in subject_map.items():
        results = frappe.get_all("Student Exam Result", filters={
            "parent": exam_id
        }, fields=["student", "student_name", "status", "marks_obtained"])

        for r in results:
            sid = r.student
            student_scores.setdefault(sid, {
                "student_name": r.student_name,
                "marks": {},
                "total": 0,
                "count": 0
            })

            marks = flt(r.marks_obtained) if r.status == "Present" else 0
            student_scores[sid]["marks"][subject] = marks
            student_scores[sid]["total"] += marks
            student_scores[sid]["count"] += 1

    # Build data
    data = []
    for sid, info in student_scores.items():
        row = [info["student_name"]]
        for subject in subjects:
            row.append(info["marks"].get(subject, 0))
        total = info["total"]
        avg = round(total / info["count"], 2) if info["count"] else 0
        row += [total, avg]
        data.append(row)

    # Ranking
    data.sort(key=lambda x: x[-2], reverse=True)
    for i, row in enumerate(data):
        row.append(i + 1)

    columns = [{"label": "Student", "fieldtype": "Data", "width": 200}]
    columns += [{"label": subject, "fieldtype": "Float", "width": 120} for subject in subjects]
    columns += [
        {"label": "Total", "fieldtype": "Float", "width": 100},
        {"label": "Average", "fieldtype": "Float", "width": 100},
        {"label": "Rank", "fieldtype": "Int", "width": 80}
    ]

    return columns, data
