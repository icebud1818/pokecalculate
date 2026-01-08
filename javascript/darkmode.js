// Dark mode toggle functionality
(function() {
    // Check for saved dark mode preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    // Create and add the dark mode toggle button
    function addDarkModeToggle() {
        const container = document.querySelector('.container');
        if (!container) return;

        const toggleButton = document.createElement('button');
        toggleButton.className = 'dark-mode-toggle';
        toggleButton.setAttribute('aria-label', 'Toggle dark mode');
        
        // Set initial icon
        updateToggleIcon(toggleButton);
        
        toggleButton.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // Save preference
            const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            localStorage.setItem('theme', theme);
            
            // Update icon
            updateToggleIcon(toggleButton);
        });
        
        container.insertBefore(toggleButton, container.firstChild);
    }

    function updateToggleIcon(button) {
        if (document.body.classList.contains('dark-mode')) {
            button.textContent = '☀️'; // Sun icon for light mode
        } else {
            button.textContent = '🌙'; // Moon icon for dark mode
        }
    }

    // Add the toggle button when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addDarkModeToggle);
    } else {
        addDarkModeToggle();
    }
})();