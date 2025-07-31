// Copyright (c) 2025, Amey Golait and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assignment Review', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button('Get Submissions', function() {
                frappe.call({
                    method: 'student_master.student_master.doctype.assignment_review.assignment_review.get_submitted_assignments',
                    args: {
                        assignment_review_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message && r.message.count) {
                            frappe.msgprint(`${r.message.count} submissions loaded.`);
                        } else {
                            frappe.msgprint("No submissions found.");
                        }
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});
