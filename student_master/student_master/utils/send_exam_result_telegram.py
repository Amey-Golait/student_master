import frappe
import requests

@frappe.whitelist()
def send_exam_result_telegram(exam_name):
    print(" ENTERED send_exam_result_telegram FUNCTION ")

    try:
        doc = frappe.get_doc("Exam", exam_name)
    except Exception as e:
        print("Error loading Exam:", str(e))
        return

    print("📘 Exam loaded:", doc.exam_name)
    print("👥 Total students:", len(doc.students))

    for row in doc.students:
        print(f"➡️ Student Row: {row.student} | Status: {row.status}")

        if row.status != "Present":
            print("⏭️ Skipping (not present)")
            continue

        try:
            student = frappe.get_doc("Student", row.student)
        except Exception as e:
            print(f"Error loading student {row.student}: {str(e)}")
            continue

        if not student.telegram_chat_id:
            print(f"No Telegram chat ID for {student.name}")
            continue

        message = (
            f"📢 *Exam Result Notification*\n"
            f"📘 *Exam Name:* {doc.exam_name}\n"
            f"👤 *Student Name:* {student.full_name}\n"
            f"🎯 *Marks:* {row.marks_obtained}/{doc.total_marks}"
        )

        try:
            send_telegram_message(student.telegram_chat_id, message)
            print(f"Message sent to {student.name}")
        except Exception as e:
            print(f"Failed to send message: {str(e)}")


def send_telegram_message(chat_id, message):
    bot_token = frappe.conf.get("telegram_bot_token")
    if not bot_token:
        raise Exception("Telegram Bot Token not configured.")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)

    if not response.ok:
        raise Exception(f"Telegram API error: {response.text}")


@frappe.whitelist()
def send_assignment_telegram(assignment_name):
    print(" ENTERED send_assignment_telegram FUNCTION ")

    try:
        doc = frappe.get_doc("Assignment", assignment_name)
    except Exception as e:
        print("Error loading Assignment:", str(e))
        return

    if not doc.class_link:
        print("No class linked to this assignment.")
        return

    students = frappe.get_all("Class Enrollment",
        filters={"class_link": doc.class_link},
        fields=["student"]
    )

    print(f"👥 Found {len(students)} students in class {doc.class_link}")

    for s in students:
        try:
            student = frappe.get_doc("Student", s.student)
        except Exception as e:
            print(f"Error loading student {s.student}: {str(e)}")
            continue

        if not student.telegram_chat_id:
            print(f"No Telegram chat ID for {student.name}")
            continue

        message = (
                f"🆕 *New Assignment Posted*\n\n"
                f"🔖 *Assignment Name:* {doc.title}\n"
                f"📘 *Subject:* {doc.subject}\n"
                f"📅 *Due Date:* {doc.due_date.strftime('%d-%b-%Y')}\n\n"
                f"Please complete and submit before the deadline."
            )

        try:
            send_telegram_message(student.telegram_chat_id, message)
            print(f"Message sent to {student.name}")
        except Exception as e:
            print(f"Failed to send message: {str(e)}")

def send_assignment_submission_telegram(submission_name):
    print(" ENTERED send_assignment_submission_telegram FUNCTION ")

    try:
        doc = frappe.get_doc("Assignment Submission", submission_name)
        print("📄 Loaded submission:", doc.name)
    except Exception as e:
        print("Error loading submission:", str(e))
        return

    try:
        student = frappe.get_doc("Student", doc.student)
        print("👤 Loaded student:", student.name)
    except Exception as e:
        print(f"Error loading student {doc.student}: {str(e)}")
        return

    try:
        assignment = frappe.get_doc("Assignment", doc.assignment)
        print("📘 Loaded assignment:", assignment.title)
    except Exception as e:
        print(f"Error loading assignment {doc.assignment}: {str(e)}")
        return

    if not student.telegram_chat_id:
        print(f"No Telegram Chat ID for {student.name}")
        return

    message = (
        f"📥 *Assignment Submitted Successfully*\n\n"
        f"📘 *Assignment:* {assignment.title}\n"
        f"👤 *Student:* {student.full_name}\n"
        f"📅 *Submitted On:* {doc.submission}\n\n"
        f"Your assignment has been recorded. Thank you!"
    )

    try:
        send_telegram_message(student.telegram_chat_id, message)
        print(f"Telegram message sent to {student.full_name}")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")

def send_assignment_review_telegram(review_name):
    print(" ENTERED send_assignment_review_telegram FUNCTION ")

    try:
        review_doc = frappe.get_doc("Assignment Review", review_name)
        print("📄 Loaded Assignment Review:", review_doc.name)
    except Exception as e:
        print("Error loading Assignment Review:", str(e))
        return

    try:
        assignment = frappe.get_doc("Assignment", review_doc.assignment)
        print("📘 Loaded assignment:", assignment.title)
    except Exception as e:
        print("Error loading Assignment:", str(e))
        return

    for row in review_doc.review_table:
        try:
            student = frappe.get_doc("Student", row.student)
            print("👤 Loaded student:", student.name)
        except Exception as e:
            print(f"Error loading student {row.student}: {str(e)}")
            continue

        if not student.telegram_chat_id:
            print(f"No Telegram Chat ID for {student.name}")
            continue

        message = (
            f"📋 *Assignment Review Completed*\n\n"
            f"📘 *Assignment:* {assignment.title}\n"
            f"👤 *Student:* {student.full_name}\n"
            f"*Grade:* {row.grade or 'Not given'}\n"
            f"💬 *Feedback:* {row.feedback or 'No feedback'}\n\n"
            f"Thank you!"
        )

        try:
            send_telegram_message(student.telegram_chat_id, message)
            print(f"Telegram message sent to {student.full_name}")
        except Exception as e:
            print(f"Failed to send message to {student.full_name}: {str(e)}")
