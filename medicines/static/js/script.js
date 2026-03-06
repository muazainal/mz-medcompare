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
});
