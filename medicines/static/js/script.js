document.addEventListener('DOMContentLoaded', () => {
    console.log('MedCompare Script Loaded');

    // --- Filter Form Auto-Submit ---
    const filterForm = document.getElementById('medicine-filter-form');
    const ratingSelect = document.getElementById('rating');
    const sortSelect = document.getElementById('sort');

    if (filterForm) {
        if (ratingSelect) {
            ratingSelect.addEventListener('change', () => {
                filterForm.submit();
            });
        }

        if (sortSelect) {
            sortSelect.addEventListener('change', () => {
                filterForm.submit();
            });
        }
    }

    // --- Signup Role Toggle ---
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
});
