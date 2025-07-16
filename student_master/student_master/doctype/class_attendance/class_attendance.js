frappe.ui.form.on('Class Attendance', {
    refresh(frm) {
        console.log('Class Attendance: refresh triggered');
        console.log('Docstatus:', frm.doc.docstatus);
        console.log('Class Link:', frm.doc.class_link);
        console.log('Academic Year:', frm.doc.academic_year);

        if (frm.doc.docstatus === 0 && frm.doc.class_link && frm.doc.academic_year) {
            frm.add_custom_button('Get Students from Class', () => {
                frappe.call({
                    method: 'student_master.student_master.doctype.class_attendance.class_attendance.get_students_from_class',
                    args: {
                        class_link: frm.doc.class_link,
                        academic_year: frm.doc.academic_year
                    },
                    callback(r) {
                        if (r.message) {
                            frm.clear_table('students');
                            r.message.forEach(student => {
                                let row = frm.add_child('students');
                                row.student = student.student;
                                row.student_name = student.student_name;
                                row.status = 'Present';
                            });
                            frm.refresh_field('students');
                            frappe.msgprint('Students loaded');
                        }
                    }
                });
            });
        } else {
            console.log('Get Students button not shown. Conditions not met.');
        }
    }
});
frappe.ui.form.on('Class Attendance', {
    setup(frm) {
        // Filter for Class Link: Only Active Classes
        frm.set_query('class_link', () => {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });

        // Filter for Academic Year: Only Active Years
        frm.set_query('academic_year', () => {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });
    }
});
