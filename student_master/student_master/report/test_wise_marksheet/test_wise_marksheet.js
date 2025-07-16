frappe.query_reports["Test Wise Marksheet"] = {
    filters: [
        {
            fieldname: "exam_id",
            label: "Any Exam Record from Test",
            fieldtype: "Link",
            options: "Exam",
            reqd: 1
        },
        {
            fieldname: "class_link",
            label: "Class",
            fieldtype: "Link",
            options: "Class",
            reqd: 1
        },
        {
            fieldname: "academic_year",
            label: "Academic Year",
            fieldtype: "Link",
            options: "Academic Year",
            reqd: 1
        }
    ]
};
