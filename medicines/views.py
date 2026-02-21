from django.shortcuts import render, get_object_or_404  # <-- added get_object_or_404
from .models import Medicine

# Home page view - list all medicines
def home(request):
    medicines = Medicine.objects.all()  # fetch all medicines from DB
    return render(request, 'medicines/home.html', {'medicines': medicines})

# Detail page for each medicine
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'medicines/medicine_detail.html', {'medicine': medicine})

# # Medicines page view - optional, could be same as home
# def medicines_list(request):
#     medicines = Medicine.objects.all()  # fetch all medicines from DB
#     return render(request, 'medicines/medicines_list.html', {'medicines': medicines})