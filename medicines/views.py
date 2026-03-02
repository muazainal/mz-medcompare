from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Medicine

# HOME PAGE
def home(request):
    # --- Get query parameters from URL ---
    search_query = request.GET.get('search', '')  # search by medicine, manufacturer, formula
    rating = request.GET.get('rating')           # filter by rating
    sort = request.GET.get('sort')               # sort by price

    # --- Base Queryset ---
    medicines = Medicine.objects.all()

    # --- SEARCH ---
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(manufacturer__name__icontains=search_query) |
            Q(formulas__name__icontains=search_query)  # using related_name
        ).distinct()

    # --- FILTER ---
    if rating:
        medicines = medicines.filter(rating__gte=rating)

    # --- SORT ---
    if sort == 'price_asc':
        medicines = medicines.order_by('price')
    elif sort == 'price_desc':
        medicines = medicines.order_by('-price')

    # --- Render Template ---
    return render(
        request,
        'medicines/medicines_list.html',
        {'medicines': medicines}
    )

# DETAIL PAGE
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(
        request,
        'medicines/medicine_detail.html',
        {'medicine': medicine}
    )