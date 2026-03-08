document.addEventListener('DOMContentLoaded', () => {

    // -----------------------------------------------
    // Navbar: add .scrolled class on scroll
    // -----------------------------------------------
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 40) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // -----------------------------------------------
    // Smooth-scroll for anchor links in hero CTAs
    // -----------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // -----------------------------------------------
    // Intersection Observer: fade-in-up animations
    // -----------------------------------------------
    const fadeEls = document.querySelectorAll('.fade-in-up');
    if (fadeEls.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    // Stagger delay based on element index within its parent
                    const siblings = Array.from(entry.target.parentElement.children);
                    const delay = siblings.indexOf(entry.target) * 80;
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        fadeEls.forEach(el => observer.observe(el));
    }

    // -----------------------------------------------
    // Filter Form: auto-submit on select change
    // -----------------------------------------------
    const filterForm = document.getElementById('medicine-filter-form');
    const ratingSelect = document.getElementById('rating');
    const sortSelect = document.getElementById('sort');

    if (filterForm) {
        if (ratingSelect) {
            ratingSelect.addEventListener('change', () => filterForm.submit());
        }
        if (sortSelect) {
            sortSelect.addEventListener('change', () => filterForm.submit());
        }
    }

    // -----------------------------------------------
    // Signup: role toggle show/hide manufacturer fields
    // -----------------------------------------------
    const userRadio = document.getElementById('role_user');
    const manufacturerRadio = document.getElementById('role_manufacturer');
    const manufacturerFields = document.getElementById('manufacturer-fields');

    if (userRadio && manufacturerRadio && manufacturerFields) {
        function toggleFields() {
            if (manufacturerRadio.checked) {
                manufacturerFields.style.display = 'block';
            } else {
                manufacturerFields.style.display = 'none';
            }
        }

        userRadio.addEventListener('change', toggleFields);
        manufacturerRadio.addEventListener('change', toggleFields);
        userRadio.addEventListener('click', toggleFields);
        manufacturerRadio.addEventListener('click', toggleFields);

        toggleFields();
    }

    // -----------------------------------------------
    // Dark Mode Toggle Switch
    // -----------------------------------------------
    const themeToggle = document.getElementById('theme-toggle');

    if (themeToggle) {
        // Initial setup for the switch state based on HTML attribute set by FOUC script
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            themeToggle.checked = true;
        }

        themeToggle.addEventListener('change', (e) => {
            const newTheme = e.target.checked ? 'dark' : 'light';

            // Apply new theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

});
