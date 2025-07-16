frappe.query_reports["Subject Wise Marksheet"] = {
    filters: [
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
