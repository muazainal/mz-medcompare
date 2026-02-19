from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
# def home(request):
#     return HttpResponse("Welcome to MedCompare! 🚀")

# Home page view
def home(request):
    # This renders home.html for the root URL
    return render(request, 'medicines/home.html')

# Medicines page view
def medicines_list(request):
    # This renders medicines_list.html for /medicines URL
    return render(request, 'medicines/medicines_list.html')