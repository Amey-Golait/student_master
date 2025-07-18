frappe.pages['student-dashboard'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '🎓 Student-Dashboard',
        single_column: true
    });

    const cards = [
        { label: "Student", route: "Student", icon: "user" },
        { label: "Class", route: "Class", icon: "layers" },
        { label: "Academic Year", route: "Academic Year", icon: "calendar" },
        { label: "Class Enrollment", route: "Class Enrollment", icon: "edit-2" },
        { label: "Class Attendance", route: "Class Attendance", icon: "check-square" },
        { label: "Exam", route: "Exam", icon: "file-text" },
        { label: "Subject Wise Marksheet", route: "Subject Wise Marksheet", type: "query-report", icon: "bar-chart-2" },
        { label: "Test Wise Marksheet", route: "Test Wise Marksheet", type: "query-report", icon: "bar-chart" },
        { label: "Annual Report Card", route: "Annual Report Card", type: "query-report", icon: "award" }
    ];

    $(wrapper).find('.layout-main-section').html(`
        <div class="dashboard-wrapper" style="padding: 1rem 1.5rem; background: linear-gradient(to right, #f8fafc, #f1f5f9); min-height: 100vh;">
            <div class="header mb-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-2">📊 Welcome to 4D Classes Dashboard</h2>
                <p class="text-gray-600">Get quick insights and navigate to key modules easily.</p>
            </div>

            <div class="dashboard-card-container grid" style="
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
                gap: 1.5rem;
                margin-bottom: 3rem;
            ">
                ${cards.map(card => get_link_card(card)).join('')}
            </div>
        </div>
    `);

    function get_link_card({ label, route, icon, type = 'List' }) {
        return `
            <div class="dashboard-card" onclick="frappe.set_route('${type}', '${route}')" style="
                padding: 1.2rem;
                border-radius: 12px;
                background: white;
                border: 1px solid #e2e8f0;
                box-shadow: 0 6px 14px rgba(0,0,0,0.05);
                cursor: pointer;
                transition: transform 0.25s ease, box-shadow 0.25s ease;
                text-align: center;
                position: relative;
            " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 18px rgba(0,0,0,0.08)'" 
              onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 14px rgba(0,0,0,0.05)'">
                <div style="font-size: 30px; color: #3b82f6; margin-bottom: 0.8rem;">
                    <i class="feather icon-${icon}"></i>
                </div>
                <div style="font-weight: 600; font-size: 16px; color: #374151;">
                    ${label}
                </div>
            </div>
        `;
    }

    if (window.feather) feather.replace();
};
