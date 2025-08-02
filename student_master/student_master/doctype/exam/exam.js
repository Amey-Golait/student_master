frappe.ui.form.on('Exam', {
    refresh(frm) {
        if (frm.doc.docstatus === 0 && frm.doc.class_link && frm.doc.academic_year) {
            frm.add_custom_button('Get Students from Class', () => {
                frappe.call({
                    method: 'student_master.student_master.doctype.exam.exam.get_students_from_class',
                    args: {
                        class_link: frm.doc.class_link,
                        academic_year: frm.doc.academic_year
                    },
                    callback(r) {
                        if (r.message) {
                            const existing = frm.doc.students.map(row => row.student);
                            r.message.forEach(student => {
                                if (!existing.includes(student.student)) {
                                    let row = frm.add_child('students');
                                    row.student = student.student;
                                    row.student_name = student.student_name;
                                    row.status = 'Present';
                                }
                            });
                            frm.refresh_field('students');
                            frappe.msgprint('Students loaded.');
                        }
                    }
                });
            });
        }
    },

    setup(frm) {
        frm.set_query('class_link', () => {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });

        frm.set_query('academic_year', () => {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });
    }
});
