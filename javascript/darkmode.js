// Dark mode toggle functionality
(function() {
    // Check for saved dark mode preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    function updateDarkModeIcon() {
        const icon = document.getElementById('darkModeIcon');
        if (icon) {
            if (document.body.classList.contains('dark-mode')) {
                icon.textContent = '☀️'; // Sun icon for light mode
            } else {
                icon.textContent = '🌙'; // Moon icon for dark mode
            }
        }
    }

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        
        // Save preference
        const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
        
        // Update icon
        updateDarkModeIcon();
    }

    // Setup sidebar dark mode toggle
    function setupSidebarToggle() {
        const sidebarToggle = document.getElementById('sidebarDarkModeToggle');
        if (sidebarToggle) {
            updateDarkModeIcon();
            sidebarToggle.addEventListener('click', toggleDarkMode);
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupSidebarToggle);
    } else {
        setupSidebarToggle();
    }
})();