frappe.ui.form.on("Assignment", {
    setup(frm) {
        frm.set_query('assigned_class', () => {
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
