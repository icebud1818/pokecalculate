// Sidebar menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const hamburgerMenu = document.getElementById('hamburgerMenu');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const closeSidebar = document.getElementById('closeSidebar');

    // Open sidebar
    hamburgerMenu.addEventListener('click', function() {
        sidebar.classList.add('active');
        sidebarOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when sidebar is open
    });

    // Close sidebar
    function closeSidebarMenu() {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
        document.body.style.overflow = ''; // Re-enable scrolling
    }

    closeSidebar.addEventListener('click', closeSidebarMenu);
    sidebarOverlay.addEventListener('click', closeSidebarMenu);

    // Close sidebar when clicking on navigation buttons
    const navigationButtons = document.querySelectorAll('.sidebar-button.orange-button, .sidebar-button.green-button, .sidebar-button.blue-button');
    navigationButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Small delay to allow navigation to complete
            setTimeout(closeSidebarMenu, 100);
        });
    });

    // Close sidebar with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebarMenu();
        }
    });
});