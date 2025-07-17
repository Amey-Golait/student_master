frappe.query_reports["Annual Report Card"] = {
    filters: [
        {
            fieldname: "student",
            label: "Student",
            fieldtype: "Link",
            options: "Student",
            reqd: 1
        }
    ]
};
