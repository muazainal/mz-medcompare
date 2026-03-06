from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Medicine, LabReport, Manufacturer
from .forms import MedicineForm

# HOME PAGE
@login_required
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
            Q(formula__icontains=search_query) |
            Q(formulas__name__icontains=search_query)
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
@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(
        request,
        'medicines/medicine_detail.html',
        {'medicine': medicine}
    )

# SIGNUP/REGISTER
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# MANUFACTURER DECORATOR
def manufacturer_required(view_func):
    def check_manufacturer(user):
        return user.groups.filter(name='Manufacturers').exists() or user.is_superuser
    return user_passes_test(check_manufacturer)(view_func)

# SUBMIT MEDICINE (Day 5 Placeholder)
@login_required
@manufacturer_required
def submit_medicine(request):
    return render(request, 'medicines/submit_medicine.html')